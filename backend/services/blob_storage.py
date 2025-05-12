import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from config.config import Config

class BlobStorageService:
    def __init__(self):
        self.config = Config()
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        self.account_name = os.getenv("AZURE_STORAGE_ACCOUNT_NAME")
        self.container_name = os.getenv("AZURE_STORAGE_CONTAINER_NAME")
        
        # Initialize BlobServiceClient
        self.blob_service_client = BlobServiceClient.from_connection_string(self.connection_string)
        
        # Create containers if they don't exist
        self._initialize_containers()

    def _initialize_containers(self):
        # Create containers for stories, audio, and images
        containers = ['stories', 'audio', 'images']
        for container in containers:
            try:
                self.blob_service_client.create_container(container)
                print(f"Created container: {container}")
            except Exception as e:
                print(f"Container {container} already exists or error occurred: {str(e)}")

    def upload_blob(self, container_name, blob_name, data):
        """
        Upload data to a specific container
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
            blob_client.upload_blob(data, overwrite=True)
            return blob_client.url
        except Exception as e:
            print(f"Error uploading blob: {str(e)}")
            raise

    def get_blob_url(self, container_name, blob_name):
        """
        Get the URL for a specific blob
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
            return blob_client.url
        except Exception as e:
            print(f"Error getting blob URL: {str(e)}")
            raise

    def delete_blob(self, container_name, blob_name):
        """
        Delete a specific blob
        """
        try:
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob= blob_name)
            blob_client.delete_blob()
        except Exception as e:
            print(f"Error deleting blob: {str(e)}")
            raise

    def list_blobs(self, container_name):
        """
        List all blobs in a container
        """
        try:
            container_client = self.blob_service_client.get_container_client(container_name)
            return [blob.name for blob in container_client.list_blobs()]
        except Exception as e:
            print(f"Error listing blobs: {str(e)}")
            raise

# Add to services/__init__.py
from .blob_storage import BlobStorageService

__all__ = ['AzureServices', 'BlobStorageService']
