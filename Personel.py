import ibm_boto3
from ibm_botocore.client import Config

# IBM Cloud credentials
# --- IMPORTANT ---
# Double-check that these values are correct and copied directly from your IBM Cloud account.
API_KEY = 'your_api_key'
SERVICE_INSTANCE_ID = 'your_service_instance_id'

# IBM Cloud Authentication Endpoint (Usually correct as is)
AUTH_ENDPOINT = 'https://iam.cloud.ibm.com/identity/token' # Common authentication endpoint

# IBM Cloud Object Storage S3 Endpoint
# --- IMPORTANT ---
# Replace 'your_cos_s3_endpoint_url' with the correct S3 endpoint for your bucket's region.
# Find endpoints here: https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-endpoints
# Example: 'https://s3.us-south.cloud-object-storage.appdomain.cloud'
COS_ENDPOINT = 'your_cos_s3_endpoint_url'

# Create IBM Cloud client
cos = ibm_boto3.client('s3',
                        ibm_api_key_id='7837709245:AAFUKbq8lRzlA3D6DKqUukq-PaGDI9T7sVI', # Enclose API key in quotes
                        ibm_service_instance_id=SERVICE_INSTANCE_ID,
                        ibm_auth_endpoint=AUTH_ENDPOINT,
                        endpoint_url=COS_ENDPOINT, # Add the S3 endpoint URL
                        config=Config(signature_version='s3v4'))
