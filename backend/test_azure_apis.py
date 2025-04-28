import os
import requests
from openai import AzureOpenAI
from dotenv import load_dotenv
import azure.cognitiveservices.speech as speechsdk

# Load environment variables
load_dotenv()

def test_dalle_api():
    """Test DALL-E API endpoint"""
    print("\n🎨 Testing DALL-E API...")
    
    endpoint = os.getenv("AZURE_DALLE_ENDPOINT")
    api_key = os.getenv("AZURE_DALLE_API_KEY")
    api_version = os.getenv("AZURE_DALLE_API_VERSION")
    
    print(f"Using DALL-E endpoint: {endpoint}")
    
    api_url = f"{endpoint}/openai/deployments/dall-e-3/images/generations?api-version={api_version}"
    
    headers = {
        "Content-Type": "application/json",
        "api-key": api_key
    }
    
    payload = {
        "prompt": "A photograph of a red fox in an autumn forest",
        "size": "1024x1024",
        "n": 1,
        "model": "dall-e-3",
        "quality": "standard",
        "style": "natural"
    }
    
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        
        if "data" in result and len(result["data"]) > 0:
            print("✅ DALL-E API test successful!")
            print(f"Response contains image data: {'url' in result['data'][0] or 'b64_json' in result['data'][0]}")
            return True
        else:
            print("❌ Unexpected response format from DALL-E API")
            print(f"Response: {result}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing DALL-E API: {str(e)}")
        return False

def test_openai_api():
    """Test OpenAI API endpoint"""
    print("\n🤖 Testing OpenAI API...")
    
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION")
    
    print(f"Using OpenAI endpoint: {endpoint}")
    print(f"Using deployment: {deployment}")
    
    try:
        client = AzureOpenAI(
            api_version=api_version,
            azure_endpoint=endpoint,
            api_key=api_key,
        )
        
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant.",
                },
                {
                    "role": "user",
                    "content": "Tell me a fun fact about space.",
                }
            ],
            model=deployment
        )
        
        print("✅ OpenAI API test successful!")
        print(f"Response: {response.choices[0].message.content}")
        return True
        
    except Exception as e:
        print(f"❌ Error testing OpenAI API: {str(e)}")
        return False

def test_speech_api():
    """Test Azure Speech Services"""
    print("\n🗣️ Testing Azure Speech Services...")
    
    speech_key = os.getenv("AZURE_SPEECH_KEY")
    speech_region = os.getenv("AZURE_SPEECH_REGION")
    
    print(f"Using Speech region: {speech_region}")
    
    try:
        # Initialize speech config
        speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=speech_region)
        
        # Create a speech synthesizer
        speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        
        # Test text-to-speech
        text = "Hello, this is a test of Azure Speech Services."
        result = speech_synthesizer.speak_text_async(text).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print("✅ Speech Services test successful!")
            return True
        else:
            print(f"❌ Speech synthesis failed: {result.reason}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing Speech Services: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting Azure API Tests...")
    
    # Test DALL-E API
    dalle_success = test_dalle_api()
    
    # Test OpenAI API
    openai_success = test_openai_api()
    
    # Test Speech API
    speech_success = test_speech_api()
    
    # Print summary
    print("\n📊 Test Summary:")
    print(f"DALL-E API: {'✅ Success' if dalle_success else '❌ Failed'}")
    print(f"OpenAI API: {'✅ Success' if openai_success else '❌ Failed'}")
    print(f"Speech API: {'✅ Success' if speech_success else '❌ Failed'}")
    
    if dalle_success and openai_success and speech_success:
        print("\n✨ All API tests completed successfully!")
    else:
        print("\n⚠️ Some tests failed. Please check your configuration.")

if __name__ == "__main__":
    main() 