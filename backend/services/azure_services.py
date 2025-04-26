from openai import AzureOpenAI
from azure.cognitiveservices.speech import SpeechConfig, SpeechSynthesizer, ResultReason
import os
from backend.config.config import Config

class AzureServices:
    def __init__(self):
        self.openai_client = AzureOpenAI(
            api_key=Config.AZURE_OPENAI_API_KEY,
            api_version=Config.AZURE_OPENAI_API_VERSION,
            azure_endpoint=Config.AZURE_OPENAI_ENDPOINT
        )
        
        self.speech_config = SpeechConfig(
            Config.AZURE_SPEECH_KEY,
            Config.AZURE_SPEECH_REGION
        )

    def generate_story(self, theme, characters, age_group):
        try:
            response = self.openai_client.chat.completions.create(
                model=Config.AZURE_OPENAI_DEPLOYMENT,
                messages=[
                    {"role": "system", "content": f"You are a creative children's story writer. Write a story appropriate for {age_group} age group."},
                    {"role": "user", "content": f"Write a story with theme: {theme} and characters: {characters}"}
                ]
            )
            return response.choices[0].message.content
        except Exception as e:
            raise Exception(f"Error generating story: {str(e)}")

    def generate_illustration(self, title, theme, characters, age_group):
        try:
            response = self.openai_client.images.generate(
                model="dall-e-3",
                prompt=f"Create a child-friendly illustration for a story titled '{title}' with theme: {theme} and characters: {characters}. The illustration should be appropriate for {age_group} age group.",
                n=1,
                size="1024x1024"
            )
            return response.data[0].url
        except Exception as e:
            raise Exception(f"Error generating illustration: {str(e)}")

    def text_to_speech(self, text):
        try:
            synthesizer = SpeechSynthesizer(speech_config=self.speech_config)
            result = synthesizer.speak_text_async(text).get()
            
            if result.reason == ResultReason.SynthesizingAudioCompleted:
                return result.audio_data
            else:
                raise Exception("Speech synthesis failed")
        except Exception as e:
            raise Exception(f"Error converting text to speech: {str(e)}") 