from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
print("Client initialized successfully.")

try:
    client.models.list()
    print("API key is valid.")
except Exception as e:
    print(f"API key is invalid: {e}")
