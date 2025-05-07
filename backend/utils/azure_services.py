import os
import logging
from azure.storage.blob import BlobServiceClient
from azure.core.exceptions import ResourceExistsError, AzureError
from azure.storage.fileshare import ShareClient
from azure.cognitiveservices.speech import SpeechConfig

logger = logging.getLogger(__name__) # Will inherit Flask app's logger config if called after app.logger is set up

def init_azure_storage(app_config):
    clients = {}
    logger.info("Starting Azure Storage initialization...")

    conn_str = app_config.get('AZURE_STORAGE_CONNECTION_STRING')
    blob_container_name = app_config.get('AZURE_STORAGE_CONTAINER_NAME', 'story-images')
    file_share_name = app_config.get('AZURE_FILE_SHARE_NAME', 'story-audio')

    logger.info(f"AZURE_STORAGE_CONNECTION_STRING is set: {bool(conn_str)}")
    if not conn_str:
        logger.error("CRITICAL: AZURE_STORAGE_CONNECTION_STRING is not set in app_config. Storage services will be unavailable.")
        return clients

    logger.info(f"Blob Container Name: {blob_container_name}")
    logger.info(f"File Share Name: {file_share_name}")

    # --- Blob Storage initialization ---
    try:
        logger.info("Initializing BlobServiceClient...")
        blob_service_client = BlobServiceClient.from_connection_string(conn_str)
        clients['blob_service_client'] = blob_service_client
        logger.info("BlobServiceClient initialized.")
        try:
            logger.info(f"Getting/creating blob container: {blob_container_name}")
            container_client = blob_service_client.get_container_client(blob_container_name)
            if not container_client.exists():
                logger.info(f"Blob container '{blob_container_name}' does not exist. Creating...")
                blob_service_client.create_container(blob_container_name)
                logger.info(f"Blob container '{blob_container_name}' created.")
            else:
                logger.info(f"Blob container '{blob_container_name}' already exists.")
            clients['blob_container_client'] = container_client
            logger.info("Azure Blob Storage component initialized successfully")
        except ResourceExistsError:
            logger.info(f"Blob container '{blob_container_name}' already exists (caught ResourceExistsError).")
            clients['blob_container_client'] = blob_service_client.get_container_client(blob_container_name) # Ensure client is set
            logger.info("Azure Blob Storage component initialized successfully")
        except AzureError as ae:
            logger.error(f"AzureError initializing Azure Blob Storage container: {str(ae)}", exc_info=True)
        except Exception as e:
            logger.error(f"Generic error initializing Azure Blob Storage container: {str(e)}", exc_info=True)
    except AzureError as ae:
        logger.error(f"AzureError failed to initialize Azure Blob Storage client: {str(ae)}", exc_info=True)
    except Exception as e:
        logger.error(f"Generic error failed to initialize Azure Blob Storage client: {str(e)}", exc_info=True)

    logger.info("-" * 30)
    logger.info("Attempting Azure File Share initialization...")
    # --- File Share initialization ---
    try:
        logger.info(f"Attempting to create ShareClient for share: '{file_share_name}'...")
        share_client = ShareClient.from_connection_string(
            conn_str=conn_str,
            share_name=file_share_name
        )
        clients['share_client'] = share_client
        logger.info("ShareClient created successfully.")
        try:
            logger.info(f"Checking if file share '{file_share_name}' exists...")
            exists = share_client.exists()
            logger.info(f"File share '{file_share_name}' exists: {exists}")
            if not exists:
                logger.info(f"File share '{file_share_name}' does not exist. Creating...")
                share_client.create_share()
                logger.info(f"File share '{file_share_name}' created.")
            logger.info("Azure File Share component initialized successfully")
        except ResourceExistsError:
            logger.info(f"File share '{file_share_name}' already exists (caught ResourceExistsError).")
            logger.info("Azure File Share component initialized successfully")
        except AzureError as ae:
            logger.error(f"AzureError during file share existence check or creation: {str(ae)}", exc_info=True)
        except Exception as e:
            logger.error(f"Generic error during file share existence check or creation: {str(e)}", exc_info=True)
    except AzureError as ae:
        logger.error(f"AzureError failed to initialize ShareClient: {str(ae)}", exc_info=True)
    except Exception as e:
        logger.error(f"Generic error failed to initialize ShareClient: {str(ae)}", exc_info=True)
    
    logger.info("Finished Azure Storage initialization attempt.")
    return clients


def init_azure_speech(app_config):
    logger.info("Initializing Azure Speech Service...")
    speech_key = app_config.get('AZURE_SPEECH_KEY')
    speech_region = app_config.get('AZURE_SPEECH_REGION')

    logger.info(f"AZURE_SPEECH_KEY is set: {bool(speech_key)}")
    logger.info(f"AZURE_SPEECH_REGION is set: {bool(speech_region)}")

    if not speech_key or not speech_region:
        logger.error("Azure Speech Key or Region not configured. Speech synthesis will be unavailable.")
        return None

    try:
        speech_config_obj = SpeechConfig(subscription=speech_key, region=speech_region)
        logger.info("Azure Speech Service configured (SpeechConfig created).")
        return speech_config_obj
    except Exception as e:
        logger.error(f"Error initializing Azure Speech Service: {str(e)}", exc_info=True)
        return None