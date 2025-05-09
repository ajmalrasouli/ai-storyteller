# backend/services/azure_services.py

import os
import logging
import sys
import traceback
import io
import requests # For downloading DALL-E image
import uuid     # For unique blob names

# Use Azure SDKs
from openai import AzureOpenAI # For DALL-E and Chat
import azure.cognitiveservices.speech as speechsdk
from azure.storage.blob import (
    BlobServiceClient,
    ContainerClient,
    ContentSettings,
    generate_container_sas,
    ContainerSasPermissions,
    generate_blob_sas,
    BlobSasPermissions,
)
from datetime import datetime, timedelta # Added ContentSettings
from azure.storage.fileshare import ShareClient
# Import the specific exceptions
from azure.core.exceptions import ResourceExistsError, ResourceNotFoundError, AzureError

logger = logging.getLogger(__name__) # Will inherit Flask app's logger config

class AzureServices:
    def __init__(self, app_config):
        """
        Initializes all Azure service clients based on the provided Flask app config.
        Args:
            app_config (werkzeug.datastructures.ImmutableDict): The Flask app.config object.
        """
        logger.info("Initializing AzureServices class...")
        self.config = app_config # Store the config object for later use if needed

        # --- Initialize Clients by calling internal methods ---
        self.text_client = self._init_openai_client()
        self.dalle_client = self._init_dalle_client()
        self.speech_config = self._init_speech_config()

        # --- Initialize storage clients and set instance attributes ---
        # The following attributes will be set by _init_azure_storage:
        self.blob_service_client = None
        self.image_container_client = None
        self.audio_container_client = None
        self.share_client = None # Keep if you still need file share access
        self._init_azure_storage() # This method now sets instance attributes

        logger.info("AzureServices class initialization finished.")
        # Logging client status now happens in create_app after initialization

    # --- Internal Initialization Methods ---

    def _init_openai_client(self):
        """Initializes the AzureOpenAI client for text/chat."""
        logger.info("Initializing Azure OpenAI Client (for Chat)...")
        api_key = self.config.get('AZURE_OPENAI_API_KEY')
        endpoint = self.config.get('AZURE_OPENAI_ENDPOINT')
        api_version = self.config.get('AZURE_OPENAI_API_VERSION') # Ensure this is set in config/env

        if not all([api_key, endpoint, api_version]):
            logger.error("Missing Azure OpenAI credentials/config for Chat (Key, Endpoint, or Version). Text generation will fail.")
            return None
        try:
            client = AzureOpenAI(
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=endpoint
            )
            logger.info("Azure OpenAI Client (Chat) initialized successfully.")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI Client (Chat): {e}", exc_info=True)
            return None

    def _init_dalle_client(self):
        """Initializes the AzureOpenAI client for DALL-E/image generation."""
        logger.info("Initializing Azure OpenAI Client (for DALL-E)...")
        api_key = self.config.get('AZURE_DALLE_API_KEY') or self.config.get('AZURE_OPENAI_API_KEY')
        endpoint = self.config.get('AZURE_DALLE_ENDPOINT') or self.config.get('AZURE_OPENAI_ENDPOINT')
        api_version = self.config.get('AZURE_DALLE_API_VERSION')

        if not all([api_key, endpoint, api_version]):
            logger.error("Missing Azure DALL-E credentials/config (Key, Endpoint, or Version). Image generation will fail.")
            return None
        try:
            client = AzureOpenAI(
                api_key=api_key,
                api_version=api_version,
                azure_endpoint=endpoint
            )
            logger.info("Azure OpenAI Client (DALL-E) initialized successfully.")
            return client
        except Exception as e:
            logger.error(f"Failed to initialize Azure OpenAI Client (DALL-E): {e}", exc_info=True)
            return None

    def _init_speech_config(self):
        """Initializes the Azure Speech SDK configuration."""
        logger.info("Initializing Azure Speech Config...")
        speech_key = self.config.get('AZURE_SPEECH_KEY')
        speech_region = self.config.get('AZURE_SPEECH_REGION')

        if not all([speech_key, speech_region]):
            logger.error("Missing Azure Speech credentials (Key or Region). Text-to-speech will fail.")
            return None
        try:
            speech_config_obj = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
            speech_config_obj.speech_synthesis_voice_name = "en-US-JennyNeural"
            speech_config_obj.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
            logger.info("Azure Speech Config initialized successfully (Voice: en-US-JennyNeural, Format: MP3).")
            return speech_config_obj
        except Exception as e:
            logger.error(f"Failed to initialize Azure Speech Config: {e}", exc_info=True)
            return None

    def _init_container(self, blob_service_client, container_name):
        """Helper to initialize a single blob container client."""
        if not blob_service_client:
            logger.error(f"Cannot initialize container '{container_name}': BlobServiceClient is not available.")
            return None
        if not container_name:
            logger.warning(f"Container name is not set, skipping initialization.")
            return None

        logger.info(f"Initializing blob container client for '{container_name}'...")
        try:
            container_client = blob_service_client.get_container_client(container_name)
            try:
                logger.info(f"Checking properties of blob container '{container_name}'...")
                container_client.get_container_properties()
                logger.info(f"Blob container '{container_name}' already exists.")
                
                # Generate SAS token for container access
                logger.info(f"Generating SAS token for container '{container_name}'")
                try:
                    sas_token = generate_container_sas(
                        account_name=self.blob_service_client.account_name,
                        container_name=container_name,
                        account_key=self.blob_service_client.credential.account_key,
                        permission=ContainerSasPermissions(read=True, list=True),
                        expiry=datetime.utcnow() + timedelta(hours=24)
                    )
                    logger.info(f"SAS token generated for container '{container_name}'")
                except Exception as e:
                    logger.error(f"Failed to generate SAS token for container '{container_name}': {e}", exc_info=True)
                    raise
            except ResourceNotFoundError:
                logger.info(f"Creating blob container '{container_name}'...")
                container_client.create_container()
                logger.info(f"Blob container '{container_name}' created.")
            except Exception as e:
                logger.error(f"Failed to set container '{container_name}' access policy: {e}", exc_info=True)
            
            return container_client
        except Exception as e:
            logger.error(f"Failed to initialize blob container '{container_name}': {e}", exc_info=True)
            return None

    def _init_azure_storage(self):
        """Initializes Azure Blob and File Share clients and stores them as instance attributes."""
        logger.info("Initializing Azure Storage clients...")
        # Attributes are already initialized to None in __init__ or will be set here

        conn_str = self.config.get('AZURE_STORAGE_CONNECTION_STRING')
        if not conn_str:
            logger.error("CRITICAL: AZURE_STORAGE_CONNECTION_STRING not set. Storage services unavailable.")
            return # Stop initialization

        # --- Blob Service Client ---
        try:
            # Store directly on self
            self.blob_service_client = BlobServiceClient.from_connection_string(conn_str)
            logger.info("BlobServiceClient initialized.")
        except Exception as e:
             logger.error(f"Failed to initialize BlobServiceClient: {e}", exc_info=True)
             return # Stop if service client fails

        # --- Specific Container Clients ---
        if self.blob_service_client:
            image_container_name = self.config.get('AZURE_IMAGES_CONTAINER_NAME', 'images')
            audio_container_name = self.config.get('AZURE_AUDIO_CONTAINER_NAME', 'audio')

            # Store results of helper directly on self
            self.image_container_client = self._init_container(self.blob_service_client, image_container_name)
            self.audio_container_client = self._init_container(self.blob_service_client, audio_container_name)
        else:
             logger.error("Cannot initialize container clients because BlobServiceClient failed.")


        # --- File Share Client (Optional) ---
        file_share_name = self.config.get('AZURE_FILE_SHARE_NAME', 'story-audio')
        if file_share_name:
            try:
                share_client_instance = ShareClient.from_connection_string(conn_str=conn_str, share_name=file_share_name)
                logger.info(f"ShareClient created for share '{file_share_name}'. Checking existence...")
                try:
                    share_client_instance.get_share_properties()
                    logger.info(f"File share '{file_share_name}' already exists.")
                except ResourceNotFoundError:
                    logger.info(f"File share '{file_share_name}' not found. Creating...")
                    share_client_instance.create_share()
                    logger.info(f"File share '{file_share_name}' created.")
                # Store directly on self
                self.share_client = share_client_instance
            except Exception as e:
                logger.error(f"Failed to initialize Azure File Share '{file_share_name}': {e}", exc_info=True)
                self.share_client = None # Ensure it's None on failure
        else:
             logger.warning("Skipping File Share initialization because AZURE_FILE_SHARE_NAME is not set.")

        # Logging moved to create_app after this method finishes
        logger.info("Finished Azure Storage initialization method.")
        # No return needed

    # --- Service Methods ---

    def generate_story(self, theme, characters, age_group):
        # ... (no changes needed in this method's logic) ...
        logger.info(f"Generating story - Theme: {theme}, Age: {age_group}")
        if not self.text_client:
            logger.error("Cannot generate story: Azure OpenAI text client not initialized.")
            return "I'm sorry, the story generation service is currently unavailable. Please try again later."
        try:
            deployment = self.config.get('AZURE_OPENAI_DEPLOYMENT_NAME')
            if not deployment:
                 logger.error("Cannot generate story: AZURE_OPENAI_DEPLOYMENT_NAME not configured.")
                 return "Error: Story generation service configuration is incomplete."

            logger.info(f"Calling OpenAI Chat API with deployment: {deployment}")
            response = self.text_client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": f"You are a creative and engaging children's story writer. Write a story appropriate for the {age_group} age group. The story should be fun, positive, and easy to understand for young children."},
                    {"role": "user", "content": f"Write a short story with the theme: '{theme}'. Include the following characters: {characters}. Make sure the story has a clear beginning, middle, and a happy or satisfying ending."}
                ],
                temperature=0.7,
                max_tokens=800
            )
            story_content = response.choices[0].message.content
            logger.info("Story generated successfully.")
            return story_content
        except Exception as e:
            logger.error(f"Error during OpenAI API call for story generation: {e}", exc_info=True)
            return f"Sorry, an error occurred while writing the story: {str(e)}"


    def generate_illustration(self, title, theme, characters, age_group):
        # ... (no changes needed in this method's logic) ...
        logger.info(f"Generating illustration for title: '{title}'")
        if not self.dalle_client:
            logger.error("Cannot generate illustration: Azure DALL-E client not initialized.")
            return None

        try:
            deployment = self.config.get('AZURE_DALLE_DEPLOYMENT_NAME')
            if not deployment:
                logger.error("Cannot generate illustration: AZURE_DALLE_DEPLOYMENT_NAME not configured.")
                return None

            prompt = f"Create a colorful and friendly cartoon illustration for a children's storybook page. The story is titled '{title}', about '{theme}' featuring '{characters}', for age group '{age_group}'. The style should be whimsical, vibrant, and suitable for young children. No text in the image."
            logger.info(f"Using DALL-E prompt (start): {prompt[:100]}...")
            logger.info(f"Using DALL-E deployment: {deployment}")

            response = self.dalle_client.images.generate(
                model=deployment,
                prompt=prompt,
                n=1,
                size="1024x1024"
            )

            image_url = response.data[0].url
            logger.info(f"Illustration generated successfully (temp URL): {image_url[:60]}...")
            return image_url # Return the temporary URL
        except Exception as e:
            logger.error(f"DALL·E illustration generation failed: {e}", exc_info=True)
            return None


    def text_to_speech(self, text):
        # ... (no changes needed in this method's logic) ...
        logger.info(f"Generating speech for text length: {len(text)}")
        if not self.speech_config:
             logger.error("Cannot generate speech: Azure Speech Config not initialized.")
             return None

        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None)

        if len(text) > 5000:
            text = text[:5000] + "..."
            logger.warning("Text truncated for speech synthesis (>5000 chars approx limit)")

        try:
            logger.info("Calling speak_text_async...")
            result = synthesizer.speak_text_async(text).get()
            logger.info(f"Speech synthesis result reason: {result.reason}")

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info("Speech synthesis successful.")
                return result.audio_data
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                logger.error(f"Speech synthesis canceled: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    logger.error(f"Cancellation Error details: {cancellation_details.error_details}")
                return None
            else:
                 logger.error(f"Speech synthesis failed with unexpected reason: {result.reason}")
                 return None

        except Exception as e:
             logger.error(f"Exception during speech synthesis: {e}", exc_info=True)
             return None


    # --- Blob Upload Helper Methods ---
    def upload_blob_from_url(self, container_client, blob_name, source_url):
        """Downloads content from a URL and uploads it as a blob."""
        if not container_client:
            logger.error(f"Cannot upload blob '{blob_name}', container client is not available.")
            return None
        logger.info(f"Downloading from {source_url[:50]}... to upload as {blob_name} in container '{container_client.container_name}'")
        try:
            response = requests.get(source_url, stream=True, timeout=30)
            response.raise_for_status()

            content_type = response.headers.get('content-type', 'image/png')
            logger.info(f"Detected content type: {content_type}")

            # Read the content into memory
            image_data = response.content
            
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.upload_blob(
                image_data,
                overwrite=True,
                content_settings=ContentSettings(content_type=content_type)
            )
            
            # Generate SAS token for the blob that lasts for 24 hours
            try:
                sas_token = generate_blob_sas(
                    account_name=self.blob_service_client.account_name,
                    container_name=container_client.container_name,
                    blob_name=blob_name,
                    account_key=self.blob_service_client.credential.account_key,
                    permission=BlobSasPermissions(read=True),
                    expiry=datetime.utcnow() + timedelta(hours=24)
                )
            except Exception as e:
                logger.error(f"Failed to generate SAS token for blob {blob_name}: {e}", exc_info=True)
                return None
            
            # Return the URL with the SAS token
            return f"https://{self.blob_service_client.account_name}.blob.core.windows.net/{container_client.container_name}/{blob_name}?{sas_token}"
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to download from URL {source_url}: {e}", exc_info=True)
            return None
        except Exception as e:
            logger.error(f"Failed to upload blob {blob_name} from URL: {e}", exc_info=True)
            return None

    def upload_blob_data(self, container_client, blob_name, data, content_type):
        """Uploads byte data as a blob."""
        if not container_client:
             logger.error(f"Cannot upload blob '{blob_name}', container client is not available.")
             return None
        logger.info(f"Uploading data as blob '{blob_name}' (size: {len(data)} bytes) to container {container_client.container_name}")
        try:
            blob_client = container_client.get_blob_client(blob_name)
            blob_client.upload_blob(
                data,
                overwrite=True,
                content_settings=ContentSettings(content_type=content_type)
                )
            logger.info(f"Successfully uploaded {blob_name} to container {container_client.container_name}.")
            return blob_client.url
        except Exception as e:
            logger.error(f"Failed to upload blob data {blob_name}: {e}", exc_info=True)
            return None