import logging
from typing import List, Optional, Any  # For type hinting

# Assuming ibm_boto3 and its exceptions are imported elsewhere or globally
# For robustness, it's better to import explicitly if not guaranteed globally
try:
    import ibm_boto3
    from ibm_botocore.client import BaseClient # For type hinting client
    from ibm_botocore.exceptions import ClientError
except ImportError:
    print("Warning: ibm-cos-sdk or ibm-botocore not found. Please install: pip install ibm-cos-sdk")
    # Define dummy types/exceptions if library isn't present, to avoid runtime errors on import
    BaseClient = type('BaseClient', (object,), {})
    ClientError = type('ClientError', (Exception,), {})

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class UserDataConnector:
    """Handles connecting to and retrieving user-specific data from IBM COS."""

    def __init__(self, cos_client: BaseClient, username: str):
        """
        Initializes the connector.

        Args:
            cos_client: An initialized ibm_boto3 S3 client instance.
            username: The username associated with the data.
        """
        self.username = username
        self.cos_client = cos_client
        self.bucket_name = f'{self.username}-data' # Define bucket name once

    def connect_to_data(self) -> List[str]:
        """Lists object keys (filenames) in the user's data bucket."""
        try:
            logger.info(f"Listing objects in bucket: {self.bucket_name}")
            objects = self.cos_client.list_objects_v2(Bucket=self.bucket_name) # Use v2 for pagination handling if needed
            # Return object keys (file names) for user data, handle empty bucket
            return [obj['Key'] for obj in objects.get('Contents', [])]
        except ClientError as e:
            logger.error(f"Error listing objects in bucket {self.bucket_name}: {e}")
            return [] # Return empty list on error

    def get_data(self, object_key: str) -> Optional[bytes]:
        """Retrieves the content of a specific object from the user's bucket."""
        try:
            logger.info(f"Getting object '{object_key}' from bucket: {self.bucket_name}")
            obj = self.cos_client.get_object(Bucket=self.bucket_name, Key=object_key)
            # Return object body (file/data content)
            return obj['Body'].read()
        except ClientError as e:
            logger.error(f"Error getting object '{object_key}' from bucket {self.bucket_name}: {e}")
            return None # Return None on error

# --- Example Usage (Requires a configured 'cos' client) ---
# Assuming 'cos' is an initialized ibm_boto3 client from Personel.py
# Uncomment the next line if 'cos' is defined in Personel.py
from Personel import cos # Make sure cos is initialized and credentials are set in Personel.py

# Check if cos client exists and run the example
if 'cos' in globals() and cos is not None:
    # Create an instance for a specific user (e.g., 'john_doe')
    # Make sure a bucket named 'john_doe-data' exists in your COS instance
    connector = UserDataConnector(cos, 'john_doe') # Pass the client

    # List files in the user's bucket
    user_data_files = connector.connect_to_data()
    print("User data files:", user_data_files)

    # Example: Try to get 'user_profile.json' if it exists
    file_to_get = 'user_profile.json'
    if file_to_get in user_data_files:
        # Get specific data file content
        data_content = connector.get_data(file_to_get)
        if data_content:
            # Assuming JSON content, decode from bytes
            try:
                import json
                print(f"\nContent of '{file_to_get}':")
                print(json.loads(data_content.decode('utf-8')))
            except (json.JSONDecodeError, UnicodeDecodeError) as decode_error:
                print(f"Could not decode '{file_to_get}' as JSON: {decode_error}")
                # print("Raw data content:", data_content) # Optionally print raw bytes
        else:
            print(f"Failed to retrieve data content for '{file_to_get}'.")
    else:
         print(f"\n'{file_to_get}' not found in the user's bucket.")
else:
     logger.error("IBM COS client ('cos') not initialized. Cannot run example usage.")
     print("Error: Ensure 'cos' client is initialized in Personel.py and credentials are set.")
