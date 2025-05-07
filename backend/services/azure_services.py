# backend/services/azure_services.py

import os
import logging
import sys
import traceback
import io

# Use Azure SDKs
from openai import AzureOpenAI # For DALL-E and Chat
import azure.cognitiveservices.speech as speechsdk
from azure.storage.blob import BlobServiceClient, ContentSettings
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
        storage_clients = self._init_azure_storage() # This returns a dict
        self.blob_service_client = storage_clients.get('blob_service_client')
        self.blob_container_client = storage_clients.get('blob_container_client')
        self.share_client = storage_clients.get('share_client')

        logger.info("AzureServices class initialization finished.")

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
        # Use specific DALL-E config keys, falling back to general OpenAI keys if needed
        api_key = self.config.get('AZURE_DALLE_API_KEY') or self.config.get('AZURE_OPENAI_API_KEY')
        endpoint = self.config.get('AZURE_DALLE_ENDPOINT') or self.config.get('AZURE_OPENAI_ENDPOINT')
        api_version = self.config.get('AZURE_DALLE_API_VERSION') # Needs specific version for DALL-E

        if not all([api_key, endpoint, api_version]):
            logger.error("Missing Azure DALL-E credentials/config (Key, Endpoint, or Version). Image generation will fail.")
            return None
        try:
            # DALL-E uses the same AzureOpenAI client class
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
            # Set a default voice (optional, can be overridden later)
            speech_config_obj.speech_synthesis_voice_name = "en-US-JennyNeural"
            # Set output format to MP3 for better web compatibility
            speech_config_obj.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
            logger.info("Azure Speech Config initialized successfully (Voice: en-US-JennyNeural, Format: MP3).")
            return speech_config_obj
        except Exception as e:
            logger.error(f"Failed to initialize Azure Speech Config: {e}", exc_info=True)
            return None

    def _init_azure_storage(self):
        """Initializes Azure Blob and File Share clients."""
        clients = {'blob_service_client': None, 'blob_container_client': None, 'share_client': None}
        logger.info("Initializing Azure Storage clients...")
        conn_str = self.config.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_container_name = self.config.get('AZURE_STORAGE_CONTAINER_NAME')
        file_share_name = self.config.get('AZURE_FILE_SHARE_NAME')

        if not conn_str:
            logger.error("CRITICAL: AZURE_STORAGE_CONNECTION_STRING not set. Storage services unavailable.")
            return clients
        if not blob_container_name:
            logger.error("CRITICAL: AZURE_STORAGE_CONTAINER_NAME not set. Blob storage unavailable.")
            # Decide if this is fatal or not
        if not file_share_name:
             logger.error("CRITICAL: AZURE_FILE_SHARE_NAME not set. File storage unavailable.")
             # Decide if this is fatal or not

        # --- Blob Storage ---
        if blob_container_name: # Only proceed if container name is set
            try:
                blob_service_client = BlobServiceClient.from_connection_string(conn_str)
                clients['blob_service_client'] = blob_service_client
                logger.info(f"BlobServiceClient initialized for container '{blob_container_name}'.")
                container_client = blob_service_client.get_container_client(blob_container_name)
                try:
                    logger.info(f"Checking properties of blob container '{blob_container_name}'...")
                    container_client.get_container_properties() # Check if exists by getting properties
                    logger.info(f"Blob container '{blob_container_name}' already exists.")
                except ResourceNotFoundError:
                    logger.info(f"Blob container '{blob_container_name}' not found. Creating...")
                    container_client.create_container()
                    logger.info(f"Blob container '{blob_container_name}' created.")
                clients['blob_container_client'] = container_client # Assign the specific container client
            except Exception as e:
                logger.error(f"Failed to initialize Azure Blob Storage for container '{blob_container_name}': {e}", exc_info=True)
                clients['blob_service_client'] = None
                clients['blob_container_client'] = None
        else:
             logger.warning("Skipping Blob Storage initialization because AZURE_STORAGE_CONTAINER_NAME is not set.")


        # --- File Share ---
        if file_share_name: # Only proceed if file share name is set
            try:
                share_client = ShareClient.from_connection_string(conn_str=conn_str, share_name=file_share_name)
                logger.info(f"ShareClient created for share '{file_share_name}'. Attempting to access properties...")
                try:
                    share_client.get_share_properties() # Try getting properties to check existence
                    logger.info(f"File share '{file_share_name}' already exists.")
                except ResourceNotFoundError:
                    logger.info(f"File share '{file_share_name}' not found. Creating...")
                    share_client.create_share()
                    logger.info(f"File share '{file_share_name}' created.")

                clients['share_client'] = share_client # Assign client if successful

            except ResourceExistsError: # Should ideally not be hit with the check above, but keep for safety
                 logger.info(f"File share '{file_share_name}' already exists (caught ResourceExistsError during create).")
                 if 'share_client' not in clients or not clients['share_client']:
                     clients['share_client'] = ShareClient.from_connection_string(conn_str=conn_str, share_name=file_share_name)

            except Exception as e:
                logger.error(f"Failed to initialize Azure File Share '{file_share_name}': {e}", exc_info=True)
                clients['share_client'] = None # Ensure client is None on any failure
        else:
             logger.warning("Skipping File Share initialization because AZURE_FILE_SHARE_NAME is not set.")


        logger.info(f"Finished Azure Storage initialization. Blob Client Ready: {bool(clients['blob_container_client'])}, Share Client Ready: {bool(clients['share_client'])}")
        return clients

    # --- Service Methods ---

    def generate_story(self, theme, characters, age_group):
        logger.info(f"Generating story - Theme: {theme}, Age: {age_group}")
        if not self.text_client:
            logger.error("Cannot generate story: Azure OpenAI text client not initialized.")
            # Provide a more user-friendly error message if possible
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
            # Consider more specific error handling if needed (e.g., rate limits, auth errors)
            return f"Sorry, an error occurred while writing the story: {str(e)}"

    def generate_illustration(self, title, theme, characters, age_group):
        logger.info(f"Generating illustration for title: '{title}'")
        if not self.dalle_client:
            logger.error("Cannot generate illustration: Azure DALL-E client not initialized.")
            return None # Indicate failure clearly

        try:
            deployment = self.config.get('AZURE_DALLE_DEPLOYMENT_NAME')
            if not deployment:
                logger.error("Cannot generate illustration: AZURE_DALLE_DEPLOYMENT_NAME not configured.")
                return None

            prompt = f"Create a colorful and friendly cartoon illustration for a children's storybook page. The story is titled '{title}', about '{theme}' featuring '{characters}', for age group '{age_group}'. The style should be whimsical, vibrant, and suitable for young children. No text in the image."
            logger.info(f"Using DALL-E prompt (start): {prompt[:100]}...")
            logger.info(f"Using DALL-E deployment: {deployment}")

            response = self.dalle_client.images.generate(
                model=deployment, # For DALL-E 3 on Azure, model is the deployment name
                prompt=prompt,
                n=1,
                size="1024x1024" # Check if your deployment supports this size
            )

            image_url = response.data[0].url
            logger.info(f"Illustration generated successfully: {image_url[:60]}...")
            return image_url
        except Exception as e:
            logger.error(f"DALL·E illustration generation failed: {e}", exc_info=True)
            # You might want to return a placeholder URL or None
            # return "/static/placeholder.png"
            return None # Indicate failure

    def text_to_speech(self, text):
        logger.info(f"Generating speech for text length: {len(text)}")
        if not self.speech_config:
             logger.error("Cannot generate speech: Azure Speech Config not initialized.")
             return None

        # Using audio_data_stream for in-memory synthesis
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None) # None -> In-memory stream

        # Basic text length check (Azure limits are more complex, depend on factors)
        if len(text) > 5000:
            text = text[:5000] + "..." # Truncate and indicate
            logger.warning("Text truncated for speech synthesis (>5000 chars approx limit)")

        try:
            logger.info("Calling speak_text_async...")
            result = synthesizer.speak_text_async(text).get() # Synchronously wait for result
            logger.info(f"Speech synthesis result reason: {result.reason}")

            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info("Speech synthesis successful.")
                return result.audio_data # Return the raw audio bytes
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation_details = result.cancellation_details
                logger.error(f"Speech synthesis canceled: {cancellation_details.reason}")
                if cancellation_details.reason == speechsdk.CancellationReason.Error:
                    logger.error(f"Cancellation Error details: {cancellation_details.error_details}")
                return None
            else: # Should not happen unless SDK adds new reasons
                 logger.error(f"Speech synthesis failed with unexpected reason: {result.reason}")
                 return None

        except Exception as e:
             logger.error(f"Exception during speech synthesis: {e}", exc_info=True)
             return None