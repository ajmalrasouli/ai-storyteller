import os
from dotenv import load_dotenv
from openai import AzureOpenAI

# Load environment variables from .env file
load_dotenv()

# Get DALL-E configuration from environment variables
api_key = os.getenv("AZURE_DALLE_API_KEY")
api_version = os.getenv("AZURE_DALLE_API_VERSION")
endpoint = os.getenv("AZURE_DALLE_ENDPOINT")
deployment_name = os.getenv("AZURE_DALLE_DEPLOYMENT_NAME")

# Debug prints
print(f"API Key: {api_key[:4]}...{api_key[-4:] if api_key else None}")
print(f"Endpoint: {endpoint}")
print(f"API Version: {api_version}")
print(f"Deployment Name: {deployment_name}")

client = AzureOpenAI(
    api_key=api_key,
    api_version=api_version,
    azure_endpoint=endpoint
)

try:
    response = client.images.generate(
        model=deployment_name,
        prompt="A cute cartoon dog wearing a space helmet",
        n=1,
        size="1024x1024"
    )
    print("\n✅ DALL-E Working!")
    print("Image URL:", response.data[0].url)
except Exception as e:
    print("\n❌ Error:", str(e))
    if hasattr(e, 'response') and hasattr(e.response, 'text'):
        print("Full error:", e.response.text)
    elif hasattr(e, 'response') and hasattr(e.response, 'json'):
        print("Full error:", e.response.json())