import os
from dotenv import load_dotenv
import requests
from openai import AzureOpenAI
import json
import azure.cognitiveservices.speech as speechsdk
import time

# Load environment variables
load_dotenv()

def validate_openai_service():
    """Validate Azure OpenAI service configuration and connectivity"""
    print("\n🔍 Validating Azure OpenAI Service...")
    
    # Get configuration
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME", "gpt-35-turbo")
    api_version = "2024-02-01"
    
    if not endpoint or not api_key:
        print("❌ Missing Azure OpenAI configuration")
        print(f"Endpoint: {'✅ Set' if endpoint else '❌ Missing'}")
        print(f"API Key: {'✅ Set' if api_key else '❌ Missing'}")
        return False
    
    try:
        # Initialize client
        client = AzureOpenAI(
            api_key=api_key,
            api_version=api_version,
            azure_endpoint=endpoint
        )
        
        # Test deployment
        print(f"Testing deployment '{deployment}'...")
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello, can you hear me?"}
            ],
            max_tokens=10
        )
        
        print("✅ Azure OpenAI Service is working correctly!")
        print(f"Deployment: {deployment}")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Error validating Azure OpenAI: {str(e)}")
        return False

def validate_dalle_service():
    """Validate Azure DALL-E service configuration and connectivity"""
    print("\n🎨 Validating Azure DALL-E Service...")
    
    # Get configuration
    endpoint = os.getenv("AZURE_DALLE_ENDPOINT")
    api_key = os.getenv("AZURE_DALLE_API_KEY")
    api_version = os.getenv("AZURE_DALLE_API_VERSION", "2024-02-01")
    
    if not endpoint or not api_key:
        print("❌ Missing Azure DALL-E configuration")
        print(f"Endpoint: {'✅ Set' if endpoint else '❌ Missing'}")
        print(f"API Key: {'✅ Set' if api_key else '❌ Missing'}")
        return False
    
    try:
        # Format URL with the correct deployment
        api_url = f"{endpoint.rstrip('/')}/openai/deployments/dall-e-3/images/generations?api-version={api_version}"
        
        # Test API
        print("Testing DALL-E API with deployment 'dall-e-3'...")
        headers = {
            "Content-Type": "application/json",
            "api-key": api_key
        }
        
        payload = {
            "prompt": "A simple test image of a smiling sun",
            "size": "256x256",
            "n": 1
        }
        
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        
        result = response.json()
        if "data" in result and len(result["data"]) > 0:
            print("✅ Azure DALL-E Service is working correctly!")
            print(f"Response contains image data: {'url' in result['data'][0] or 'b64_json' in result['data'][0]}")
            return True
        else:
            print("❌ Unexpected response format from DALL-E API")
            return False
            
    except Exception as e:
        print(f"❌ Error validating Azure DALL-E: {str(e)}")
        return False

def validate_speech_service():
    """Validate Azure Speech Services configuration and connectivity"""
    print("\n🎤 Validating Azure Speech Services...")
    
    # Get configuration
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")
    
    if not speech_key or not speech_region:
        print("❌ Missing Azure Speech Services configuration")
        print(f"Speech Key: {'✅ Set' if speech_key else '❌ Missing'}")
        print(f"Speech Region: {'✅ Set' if speech_region else '❌ Missing'}")
        return False
    
    try:
        # Test Text-to-Speech
        print("Testing Text-to-Speech...")
        speech_config = speechsdk.SpeechConfig(
            subscription=speech_key,
            region=speech_region
        )
        
        # Set the voice
        speech_config.speech_synthesis_voice_name = "en-US-JennyNeural"
        
        # Create a speech synthesizer
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        
        # Test synthesis
        result = speech_synthesizer.speak_text_async("Hello, this is a test of Azure Speech Services.").get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("✅ Text-to-Speech is working correctly!")
        else:
            print(f"❌ Text-to-Speech failed: {result.reason}")
            return False
        
        # Test Speech-to-Text
        print("Testing Speech-to-Text...")
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        speech_recognizer = speechsdk.SpeechRecognizer(
            speech_config=speech_config,
            audio_config=audio_config
        )
        
        print("Please speak into your microphone...")
        result = speech_recognizer.recognize_once_async().get()
        
        if result.reason == speechsdk.ResultReason.RecognizedSpeech:
            print("✅ Speech-to-Text is working correctly!")
            print(f"Recognized: {result.text}")
        elif result.reason == speechsdk.ResultReason.NoMatch:
            print("❌ Speech-to-Text: No speech could be recognized")
            return False
        else:
            print(f"❌ Speech-to-Text failed: {result.reason}")
            return False
            
        return True
            
    except Exception as e:
        print(f"❌ Error validating Azure Speech Services: {str(e)}")
        return False

def main():
    """Main validation function"""
    print("🚀 Starting Azure AI Services Validation...")
    
    # Validate OpenAI
    openai_valid = validate_openai_service()
    
    # Validate DALL-E
    dalle_valid = validate_dalle_service()
    
    # Validate Speech Services
    speech_valid = validate_speech_service()
    
    # Print summary
    print("\n📊 Validation Summary:")
    print(f"Azure OpenAI: {'✅ Working' if openai_valid else '❌ Not Working'}")
    print(f"Azure DALL-E: {'✅ Working' if dalle_valid else '❌ Not Working'}")
    print(f"Azure Speech: {'✅ Working' if speech_valid else '❌ Not Working'}")
    
    if openai_valid and dalle_valid and speech_valid:
        print("\n✨ All Azure AI services are working correctly!")
    else:
        print("\n⚠️ Some services are not working. Please check your configuration.")

if __name__ == "__main__":
    main() 