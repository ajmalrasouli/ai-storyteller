import os
from openai import AzureOpenAI
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Azure-specific values
endpoint = "https://ajmal-m9psmmwe-eastus2.openai.azure.com/"
deployment = "gpt-4.1-mini"
api_version = "2024-12-01-preview"
subscription_key = os.getenv("AZURE_OPENAI_API_KEY")

# Init client
client = AzureOpenAI(
    api_key=subscription_key,
    api_version=api_version,
    azure_endpoint=endpoint,
)

# Test call
response = client.chat.completions.create(
    model=deployment,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Tell me a fun fact about space."}
    ]
)

print(response.choices[0].message.content)
