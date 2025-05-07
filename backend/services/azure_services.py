import os
import logging
import sys
import traceback
import io

# Use Azure SDKs
from openai import AzureOpenAI # For DALL-E and potentially Chat if using v1+ SDK style
import azure.cognitiveservices.speech as speechsdk
from azure.storage.blob import BlobServiceClient, ContentSettings
from azure.storage.fileshare import ShareClient
from azure.core.exceptions import ResourceExistsError, AzureError

logger = logging.getLogger(__name__)

class AzureServices:
    def __init__(self, app_config):
        logger.info("Initializing AzureServices class...")
        self.config = app_config # Store the config object

        # --- Initialize Clients ---
        self.text_client = self._init_openai_client()
        self.dalle_client = self._init_dalle_client()
        self.speech_config = self._init_speech_config()
        storage_clients = self._init_azure_storage()
        self.blob_service_client = storage_clients.get('blob_service_client')
        self.blob_container_client = storage_clients.get('blob_container_client')
        self.share_client = storage_clients.get('share_client')

        logger.info("AzureServices class initialization finished.")

    def _init_openai_client(self):
        logger.info("Initializing Azure OpenAI Client (for Chat)...")
        api_key = self.config.get('AZURE_OPENAI_API_KEY')
        endpoint = self.config.get('AZURE_OPENAI_ENDPOINT')
        api_version = self.config.get('AZURE_OPENAI_API_VERSION')

        if not all([api_key, endpoint, api_version]):
            logger.error("Missing Azure OpenAI credentials/config for Chat. Text generation will fail.")
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
        logger.info("Initializing Azure OpenAI Client (for DALL-E)...")
        api_key = self.config.get('AZURE_DALLE_API_KEY')
        endpoint = self.config.get('AZURE_DALLE_ENDPOINT')
        api_version = self.config.get('AZURE_DALLE_API_VERSION')

        # Note: DALL-E 3 via Azure OpenAI requires specific API versions (e.g., "2024-02-01")
        # and the endpoint might be the same as the chat one.
        if not all([api_key, endpoint, api_version]):
            logger.error("Missing Azure DALL-E credentials/config. Image generation will fail.")
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
        logger.info("Initializing Azure Speech Config...")
        speech_key = self.config.get('AZURE_SPEECH_KEY')
        speech_region = self.config.get('AZURE_SPEECH_REGION')

        if not all([speech_key, speech_region]):
            logger.error("Missing Azure Speech credentials. Text-to-speech will fail.")
            return None
        try:
            speech_config_obj = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
            # Set a default voice (optional)
            speech_config_obj.speech_synthesis_voice_name = "en-US-JennyNeural"
            logger.info("Azure Speech Config initialized successfully.")
            return speech_config_obj
        except Exception as e:
            logger.error(f"Failed to initialize Azure Speech Config: {e}", exc_info=True)
            return None

    def _init_azure_storage(self):
        clients = {'blob_service_client': None, 'blob_container_client': None, 'share_client': None}
        logger.info("Initializing Azure Storage clients...")
        conn_str = self.config.get('AZURE_STORAGE_CONNECTION_STRING')
        blob_container_name = self.config.get('AZURE_STORAGE_CONTAINER_NAME')
        file_share_name = self.config.get('AZURE_FILE_SHARE_NAME')

        if not conn_str:
            logger.error("CRITICAL: AZURE_STORAGE_CONNECTION_STRING not set. Storage services unavailable.")
            return clients

        # --- Blob Storage ---
        try:
            blob_service_client = BlobServiceClient.from_connection_string(conn_str)
            clients['blob_service_client'] = blob_service_client
            logger.info("BlobServiceClient initialized.")
            container_client = blob_service_client.get_container_client(blob_container_name)
            if not container_client.exists():
                logger.info(f"Creating blob container '{blob_container_name}'...")
                container_client.create_container()
                logger.info(f"Blob container '{blob_container_name}' created.")
            else:
                 logger.info(f"Blob container '{blob_container_name}' already exists.")
            clients['blob_container_client'] = container_client
        except Exception as e:
            logger.error(f"Failed to initialize Azure Blob Storage: {e}", exc_info=True)
            clients['blob_service_client'] = None # Ensure clients are None on failure
            clients['blob_container_client'] = None

        # --- File Share ---
        try:
            share_client = ShareClient.from_connection_string(conn_str=conn_str, share_name=file_share_name)
            if not share_client.exists():
                 logger.info(f"Creating file share '{file_share_name}'...")
                 share_client.create_share()
                 logger.info(f"File share '{file_share_name}' created.")
            else:
                 logger.info(f"File share '{file_share_name}' already exists.")
            clients['share_client'] = share_client
        except Exception as e:
            logger.error(f"Failed to initialize Azure File Share: {e}", exc_info=True)
            clients['share_client'] = None # Ensure client is None on failure

        logger.info(f"Finished Azure Storage initialization. Blob Client: {bool(clients['blob_container_client'])}, Share Client: {bool(clients['share_client'])}")
        return clients

    # --- Service Methods ---

    def generate_story(self, theme, characters, age_group):
        logger.info(f"Generating story - Theme: {theme}, Age: {age_group}")
        if not self.text_client:
            logger.error("Cannot generate story: Azure OpenAI text client not initialized.")
            return "Error: Story generation service is not available."
        try:
            deployment = self.config.get('AZURE_OPENAI_DEPLOYMENT_NAME')
            if not deployment:
                 logger.error("Cannot generate story: AZURE_OPENAI_DEPLOYMENT_NAME not configured.")
                 return "Error: Story generation model not configured."

            logger.info(f"Calling OpenAI with deployment: {deployment}")
            response = self.text_client.chat.completions.create(
                model=deployment,
                messages=[
                    {"role": "system", "content": f"You are a creative and engaging children's story writer. Write a story appropriate for the {age_group} age group. The story should be fun, positive, and easy to understand for young children."},
                    {"role": "user", "content": f"Write a short story with the theme: '{theme}'. Include the following characters: {characters}. Make sure the story has a clear beginning, middle, and a happy or satisfying ending."}
                ],
                temperature=0.7,
                max_tokens=800 # Adjust as needed
            )
            story_content = response.choices[0].message.content
            logger.info("Story generated successfully.")
            return story_content
        except Exception as e:
            logger.error(f"Error generating story: {e}", exc_info=True)
            return f"Error generating story: {str(e)}"

    def generate_illustration(self, title, theme, characters, age_group):
        logger.info(f"Generating illustration for title: '{title}'")
        if not self.dalle_client:
            logger.error("Cannot generate illustration: Azure DALL-E client not initialized.")
            return None # Return None or a placeholder path string

        try:
            deployment = self.config.get('AZURE_DALLE_DEPLOYMENT_NAME')
            if not deployment:
                logger.error("Cannot generate illustration: AZURE_DALLE_DEPLOYMENT_NAME not configured.")
                return None

            # Improved prompt for DALL-E
            prompt = f"Create a colorful and friendly cartoon illustration for a children's storybook page. The story is titled '{title}', about '{theme}' featuring '{characters}', for age group '{age_group}'. The style should be whimsical, vibrant, and suitable for young children. No text in the image."
            logger.info(f"Using DALL-E prompt (start): {prompt[:100]}...")
            logger.info(f"Using DALL-E deployment: {deployment}")

            response = self.dalle_client.images.generate(
                model=deployment, # Use deployment name for Azure DALL-E 3
                prompt=prompt,
                n=1,
                size="1024x1024" # Ensure this size is supported by your DALL-E deployment
            )

            image_url = response.data[0].url
            logger.info(f"Illustration generated successfully: {image_url[:60]}...")
            return image_url
        except Exception as e:
            logger.error(f"DALL·E illustration generation failed: {e}", exc_info=True)
            return None # Indicate failure

    def text_to_speech(self, text):
        logger.info(f"Generating speech for text length: {len(text)}")
        if not self.speech_config:
             logger.error("Cannot generate speech: Azure Speech Config not initialized.")
             return None # Return None to indicate failure

        # Use AudioDataStream for in-memory processing
        # Setting output format can improve compatibility
        self.speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz32KBitRateMonoMp3)
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config, audio_config=None) # Use None for in-memory stream

        if len(text) > 5000: # Basic check, Azure might have stricter limits depending on voice/tier
            text = text[:5000]
            logger.warning("Text truncated for speech synthesis (>5000 chars)")

        result = synthesizer.speak_text_async(text).get()

        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            logger.info("Speech synthesis successful.")
            # The audio data is in result.audio_data
            return result.audio_data
        elif result.reason == speechsdk.ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            logger.error(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == speechsdk.CancellationReason.Error:
                logger.error(f"Error details: {cancellation_details.error_details}")
            return None
        else:
             logger.error(f"Speech synthesis failed with reason: {result.reason}")
             return None