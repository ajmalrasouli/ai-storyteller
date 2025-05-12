import openai
import azure.cognitiveservices.speech as speechsdk
import os
from config.config import Config
from openai import AzureOpenAI
from services.blob_storage import BlobStorageService

class AzureServices:
    def __init__(self):
        # Initialize Blob Storage
        self.config = Config()
        self.blob_storage = BlobStorageService()
        
        # GPT (text) configuration
        self.openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.openai_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        
        # Initialize Azure OpenAI client for text generation
        self.text_client = AzureOpenAI(
            api_key=self.openai_api_key,
            api_version=self.openai_api_version,
            azure_endpoint=self.openai_endpoint
        )
        
        # Speech Services configuration
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.speech_region = os.getenv("AZURE_SPEECH_REGION")
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key,
            region=self.speech_region
        )
        # Set speech synthesis voice
        self.speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
        
        # Initialize container names from config
        self.container_names = {
            'stories': self.config.AZURE_STORAGE_CONTAINER_STORIES,
            'audio': self.config.AZURE_STORAGE_CONTAINER_AUDIO,
            'images': self.config.AZURE_STORAGE_CONTAINER_IMAGES
        }
        
        # DALL-E (image) configuration
        self.dalle_api_key = os.getenv("AZURE_DALLE_API_KEY")
        self.dalle_endpoint = os.getenv("AZURE_DALLE_ENDPOINT")
        self.dalle_deployment_name = os.getenv("AZURE_DALLE_DEPLOYMENT_NAME")
        self.dalle_api_version = os.getenv("AZURE_DALLE_API_VERSION")
        
        # Debug prints for env vars (mask sensitive parts)
        print("[AzureServices] AZURE_OPENAI_API_KEY:", (self.openai_api_key[:4] + "..." + self.openai_api_key[-4:]) if self.openai_api_key else None)
        print("[AzureServices] AZURE_OPENAI_ENDPOINT:", self.openai_endpoint)
        print("[AzureServices] AZURE_OPENAI_DEPLOYMENT_NAME:", self.openai_deployment_name)
        print("[AzureServices] AZURE_OPENAI_API_VERSION:", self.openai_api_version)
        print("[AzureServices] AZURE_DALLE_API_KEY:", (self.dalle_api_key[:4] + "..." + self.dalle_api_key[-4:]) if self.dalle_api_key else None)
        print("[AzureServices] AZURE_DALLE_ENDPOINT:", self.dalle_endpoint)
        print("[AzureServices] AZURE_DALLE_DEPLOYMENT_NAME:", self.dalle_deployment_name)
        print("[AzureServices] AZURE_DALLE_API_VERSION:", self.dalle_api_version)
        print("[AzureServices] AZURE_SPEECH_KEY:", (self.speech_key[:4] + "..." + self.speech_key[-4:]) if self.speech_key else None)
        print("[AzureServices] AZURE_SPEECH_REGION:", self.speech_region)

    def generate_story(self, theme, characters, age_group):
        """
        Generate a story using GPT based on the provided theme, characters, and age group.
        """
        try:
            prompt = f"Write a children's story for the following theme: {theme}. Characters: {', '.join(characters)}. Age group: {age_group}. Make it fun, imaginative, and age-appropriate."
            print(f"[GPT] Generating story with prompt: {prompt}")
            response = self.text_client.chat.completions.create(
                model=self.openai_deployment_name,
                messages=[{"role": "system", "content": "You are a creative children's storyteller."},
                          {"role": "user", "content": prompt}],
                max_tokens=600,
                temperature=0.8
            )
            story_content = response.choices[0].message.content
            print(f"[GPT] Story generated successfully.")
            return story_content
        except Exception as e:
            print(f"[GPT ERROR] Failed to generate story: {str(e)}")
            raise Exception(f"Error generating story: {str(e)}")

    def generate_illustration(self, title, theme, characters, age_group):
        """
        Generate an illustration using DALL-E
        """
        try:
            import sys
            print(f"[DALLE] Starting illustration generation for title: '{title}'", file=sys.stderr)
            print(f"[DALLE] Using API key: {self.dalle_api_key[:4]}...{self.dalle_api_key[-4:] if self.dalle_api_key else None}", file=sys.stderr)
            print(f"[DALLE] Using endpoint: {self.dalle_endpoint}", file=sys.stderr)
            print(f"[DALLE] Using deployment: {self.dalle_deployment_name}", file=sys.stderr)
            print(f"[DALLE] Using API version: {self.dalle_api_version}", file=sys.stderr)
            print(f"[DALLE] Using model: {self.dalle_model}")

            # Create a simple, child-friendly prompt
            prompt = f"Draw a happy, cartoon-style illustration of {', '.join(characters)} in a {theme} setting. "
            prompt += "Use bright, cheerful colors and keep the style simple and friendly. "
            prompt += "Make sure the image is safe and appropriate for children aged 3-5."
            
            print(f"[DALLE] Using prompt: \n{prompt}")

            # Initialize DALL-E client
            client = openai.OpenAI(
                api_key=self.dalle_api_key,
                api_base=self.dalle_endpoint,
                api_version=self.dalle_api_version
            )

            # Generate image
            response = client.images.generate(
                model=self.dalle_model,
                prompt=prompt,
                n=1,
                size="1024x1024",
                response_format="url"
            )

            # Get image URL
            image_url = response.data[0].url
            print(f"[DALLE] Successfully generated image URL: {image_url}")

            return image_url

        except Exception as e:
            print(f"[DALLE ERROR] Failed to generate illustration: {str(e)}")
            raise Exception(f"Error generating illustration: {str(e)}")

    def save_story_content(self, story_content, title):
        """
        Save story content to Azure Blob Storage with proper SAS token handling
        """
        try:
            # Convert story content to bytes
            content_bytes = story_content.encode('utf-8')
            
            # Generate a unique filename
            filename = f"story_{title.replace(' ', '_')}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.txt"
            
            # Upload to blob storage
            url = self.blob_storage.upload_blob(
                self.container_names['stories'],
                filename,
                content_bytes,
                content_type='text/plain'
            )
            
            print(f"Successfully saved story content to: {url}")
            return url
        except Exception as e:
            print(f"Error saving story content: {str(e)}")
            import traceback
            print("Stack trace:")
            print(traceback.format_exc())
            raise

    def save_image(self, image_data, title):
        """
        Save image to Azure Blob Storage with proper SAS token handling
        """
        try:
            # Ensure image data is in bytes
            if isinstance(image_data, str):
                # If it's a URL, download the image
                import requests
                from io import BytesIO
                response = requests.get(image_data)
                image_data = BytesIO(response.content).getvalue()
            
            # Generate a unique filename
            filename = f"{title.replace(' ', '_')}_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.png"
            
            # Upload to blob storage
            url = self.blob_storage.upload_blob(
                self.container_names['images'],
                filename,
                image_data,
                content_type='image/png'
            )
            
            print(f"Successfully saved image to: {url}")
            return url
        except Exception as e:
            print(f"Error saving image: {str(e)}")
            import traceback
            print("Stack trace:")
            print(traceback.format_exc())
            raise

    def text_to_speech(self, text):
        """
        Convert text to speech using Azure Speech Services
        """
        try:
            # Create audio configuration
            audio_config = speechsdk.audio.AudioOutputConfig(use_default_speaker=True)
            
            # Create speech synthesizer
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=self.speech_config,
                audio_config=audio_config
            )
            
            # Synthesize speech
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print("Speech synthesis completed successfully")
                return result.audio_data
            else:
                print(f"Speech synthesis failed: {result.reason}")
                raise Exception(f"Speech synthesis failed: {result.reason}")
                
        except Exception as e:
            print(f"Error in text_to_speech: {str(e)}")
            raise
