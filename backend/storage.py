# storage.py
import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
import uuid

class AzureStorageManager:
    def __init__(self):
        connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.blob_service_client = BlobServiceClient.from_connection_string(connection_string)
        
    def upload_story_text(self, story_text, story_id):
        """Upload story text to blob storage"""
        container_client = self.blob_service_client.get_container_client("stories")
        blob_name = f"{story_id}.txt"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(story_text, overwrite=True)
        return blob_name
        
    def upload_image(self, image_data, story_id):
        """Upload story image to blob storage"""
        container_client = self.blob_service_client.get_container_client("images")
        blob_name = f"{story_id}.png"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(image_data, overwrite=True)
        return blob_name
        
    def upload_audio(self, audio_data, story_id):
        """Upload story audio to blob storage"""
        container_client = self.blob_service_client.get_container_client("audio")
        blob_name = f"{story_id}.mp3"
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob(audio_data, overwrite=True)
        return blob_name
        
    def get_story_text(self, blob_name):
        """Get story text from blob storage"""
        container_client = self.blob_service_client.get_container_client("stories")
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall().decode("utf-8")
        
    def get_image(self, blob_name):
        """Get image from blob storage"""
        container_client = self.blob_service_client.get_container_client("images")
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall()
        
    def get_audio(self, blob_name):
        """Get audio from blob storage"""
        container_client = self.blob_service_client.get_container_client("audio")
        blob_client = container_client.get_blob_client(blob_name)
        return blob_client.download_blob().readall()