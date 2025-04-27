import openai
import azure.cognitiveservices.speech as speechsdk
import os
from config.config import Config

class AzureServices:
    def __init__(self):
        # GPT (text) configuration
        self.openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
        self.openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
        self.openai_deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
        self.openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
        
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
        
        # Configure OpenAI for Azure
        openai.api_type = "azure"
        openai.api_key = self.openai_api_key
        openai.api_base = self.openai_endpoint
        openai.api_version = self.openai_api_version
        
        # Speech Services configuration
        self.speech_key = os.getenv("AZURE_SPEECH_KEY")
        self.speech_region = os.getenv("AZURE_SPEECH_REGION")
        print("[AzureServices] AZURE_SPEECH_KEY:", (self.speech_key[:4] + "..." + self.speech_key[-4:]) if self.speech_key else None)
        print("[AzureServices] AZURE_SPEECH_REGION:", self.speech_region)
        
        self.speech_config = speechsdk.SpeechConfig(
            subscription=self.speech_key,
            region=self.speech_region
        )
        # Set speech synthesis voice
        self.speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"

    def generate_story(self, theme, characters, age_group):
        try:
            response = openai.ChatCompletion.create(
                engine=self.openai_deployment_name,
                messages=[
                    {"role": "system", "content": f"You are a creative children's story writer. Write a story appropriate for {age_group} age group."},
                    {"role": "user", "content": f"Write a story with theme: {theme} and characters: {characters}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating story: {str(e)}")

    def generate_illustration(self, title, theme, characters, age_group):
        import sys
        print(f"[DALLE] Starting illustration generation for title: '{title}'", file=sys.stderr)
        print(f"[DALLE] Using API key: {self.dalle_api_key[:4]}...{self.dalle_api_key[-4:] if self.dalle_api_key else None}", file=sys.stderr)
        print(f"[DALLE] Using endpoint: {self.dalle_endpoint}", file=sys.stderr)
        print(f"[DALLE] Using deployment: {self.dalle_deployment_name}", file=sys.stderr)
        print(f"[DALLE] Using API version: {self.dalle_api_version}", file=sys.stderr)
        
        try:
            # Create a more detailed, child-friendly prompt
            prompt = f"Create a colorful, child-friendly, cartoon-style illustration for a children's story titled '{title}'. The story has theme: {theme} and features characters: {characters}. The illustration should be bright, engaging, and appropriate for {age_group} age group. Emphasize friendly interactions, no violence or scary elements; make it cute and playful for young children."
            
            print(f"[DALLE] Using prompt: {prompt[:100]}...", file=sys.stderr)
            
            # Use the DALL-E specific client
            # Set Azure OpenAI config for DALL·E
            openai.api_type = "azure"
            openai.api_base = self.dalle_endpoint
            openai.api_version = self.dalle_api_version
            openai.api_key = self.dalle_api_key
            print(f"[DALLE] openai.api_type: {openai.api_type}", file=sys.stderr)
            print(f"[DALLE] openai.api_base: {openai.api_base}", file=sys.stderr)
            print(f"[DALLE] openai.api_version: {openai.api_version}", file=sys.stderr)
            print(f"[DALLE] openai.api_key: {openai.api_key[:4]}...{openai.api_key[-4:] if openai.api_key else None}", file=sys.stderr)
            print(f"[DALLE] Using engine: {self.dalle_deployment_name}", file=sys.stderr)
            response = openai.Image.create(
                engine=self.dalle_deployment_name,
                prompt=prompt,
                n=1,
                size="1024x1024"
            )
            
            # Get the image URL
            image_url = response.data[0].url
            print(f"[DALLE] Successfully generated image: {image_url[:50]}...", file=sys.stderr)
            return image_url
            
        except Exception as e:
            import traceback
            print(f"[DALLE ERROR] Failed to generate illustration: {str(e)}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)
            raise Exception(f"Error generating illustration: {str(e)}")


    def text_to_speech(self, text):
        try:
            print(f"[AzureServices] Generating speech for text of length: {len(text)}")
            # Create a speech synthesizer using the configured speech config
            synthesizer = speechsdk.SpeechSynthesizer(speech_config=self.speech_config)
            
            # Limit text length if needed (Azure has limits)
            if len(text) > 5000:
                text = text[:5000] + "..."
                print("[AzureServices] Text truncated for speech synthesis (>5000 chars)")
            
            # Generate speech
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                print("[AzureServices] Speech synthesis successful")
                return result.audio_data
            else:
                print(f"[AzureServices] Speech synthesis failed with reason: {result.reason}")
                raise Exception(f"Speech synthesis failed with reason: {result.reason}")
        except Exception as e:
            print(f"[AzureServices] Error in text_to_speech: {str(e)}")
            raise Exception(f"Error converting text to speech: {str(e)}")
 