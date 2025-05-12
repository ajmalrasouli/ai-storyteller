import os
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient
from config.config import Config

class BlobStorageService:
    def __init__(self):
        self.config = Config()
        self.connection_string = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
        
        # Parse account name from connection string
        if self.connection_string:
            self.account_name = self.connection_string.split("AccountName=")[1].split(";")[0]
            self.account_key = self.connection_string.split("AccountKey=")[1].split(";")[0]
        else:
            raise ValueError("AZURE_STORAGE_CONNECTION_STRING environment variable is not set")
        
        # Initialize BlobServiceClient with account name and key
        self.blob_service_client = BlobServiceClient(
            account_url=f"https://{self.account_name}.blob.core.windows.net",
            credential=self.account_key
        )
        
        # Create containers if they don't exist
        self._initialize_containers()

    def _initialize_containers(self):
        """
        Initialize all required containers with proper access levels
        """
        try:
            # Get or create containers
            for container_name in ['stories', 'audio', 'images']:
                container_client = self.blob_service_client.get_container_client(container_name)
                if not container_client.exists():
                    container_client.create_container()
                    print(f"Created container: {container_name}")
                else:
                    print(f"Container {container_name} already exists")
                    
                # Set access policy for images container
                if container_name == 'images':
                    try:
                        # Get current policy
                        policy = container_client.get_container_access_policy()
                        # Set public access if not already set
                        if not policy['public_access'] == 'container':
                            container_client.set_container_access_policy(
                                public_access='container'
                            )
                            print(f"Set public access for container: {container_name}")
                    except Exception as e:
                        print(f"Error setting access policy for {container_name}: {str(e)}")
        except Exception as e:
            print(f"Error initializing containers: {str(e)}")
            raise

    def upload_blob(self, container_name, blob_name, data, content_type=None):
        """
        Upload data to a specific container with proper content type and SAS token
        """
        try:
            print(f"\n=== Starting blob upload ===")
            print(f"Container: {container_name}")
            print(f"Blob name: {blob_name}")
            
            # Set content type based on container or provided type
            if content_type is None:
                content_type_map = {
                    'images': 'image/png',
                    'audio': 'audio/mpeg',
                    'stories': 'text/plain'
                }
                content_type = content_type_map.get(container_name, 'application/octet-stream')
            
            print(f"Content type: {content_type}")
            print(f"Data length: {len(data)} bytes")
            
            # Get blob client
            blob_client = self.blob_service_client.get_blob_client(container=container_name, blob=blob_name)
            print(f"Blob client URL: {blob_client.url}")
            
            # Create proper content settings object
            from azure.storage.blob import ContentSettings
            
            # Upload blob with content settings
            blob_client.upload_blob(
                data, 
                overwrite=True,
                content_settings=ContentSettings(
                    content_type=content_type
                )
            )
            print(f"Successfully uploaded blob")
            
            # Generate SAS token for the blob
            sas_token = blob_client.generate_sas(
                permission="r",
                expiry=datetime.utcnow() + timedelta(days=365),
                start=datetime.utcnow()
            )
            
            # Return URL with SAS token
            url = f"{blob_client.url}?{sas_token}"
            print(f"Generated URL with SAS: {url}")
            return url
        except Exception as e:
            print(f"\n=== Error uploading blob ===")
            print(f"Error: {str(e)}")
            import traceback
            print("Stack trace:")
            print(traceback.format_exc())
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
