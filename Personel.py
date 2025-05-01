import ibm_boto3
from ibm_botocore.client import Config
import os # Import the os module

# IBM Cloud credentials
# --- IMPORTANT ---
# Load credentials from environment variables for better security
# Ensure you set these variables in your environment before running the script:
# $env:IBM_API_KEY="your_actual_api_key"
# $env:IBM_SERVICE_INSTANCE_ID="your_actual_crn"
# $env:IBM_COS_ENDPOINT="your_actual_s3_endpoint"

API_KEY = os.environ.get('IBM_API_KEY')
SERVICE_INSTANCE_ID = os.environ.get('IBM_SERVICE_INSTANCE_ID')
COS_ENDPOINT = os.environ.get('IBM_COS_ENDPOINT')

# IBM Cloud Authentication Endpoint (Usually correct as is)
AUTH_ENDPOINT = 'https://iam.cloud.ibm.com/identity/token' # Common authentication endpoint

# IBM Cloud Object Storage S3 Endpoint
# --- IMPORTANT ---
# Replace 'your_cos_s3_endpoint_url' with the correct S3 endpoint for your bucket's region.
# Find endpoints here: https://cloud.ibm.com/docs/cloud-object-storage?topic=cloud-object-storage-endpoints
# Example: 'https://s3.us-south.cloud-object-storage.appdomain.cloud'
# COS_ENDPOINT = 'https://s3.REGION.cloud-object-storage.appdomain.cloud' # <-- Replace this placeholder with your actual S3 endpoint URL

# Check if credentials were loaded
if not all([API_KEY, SERVICE_INSTANCE_ID, COS_ENDPOINT]):
    print("Error: Missing IBM Cloud credentials or endpoint in environment variables.")
    print("Please set IBM_API_KEY, IBM_SERVICE_INSTANCE_ID, and IBM_COS_ENDPOINT.")
    cos = None # Set cos to None if credentials are missing
else:
    # Create IBM Cloud client
    cos = ibm_boto3.client('s3',
                            ibm_api_key_id=API_KEY, # Use the API_KEY variable
                            ibm_service_instance_id=SERVICE_INSTANCE_ID, # Use the SERVICE_INSTANCE_ID variable
                            ibm_auth_endpoint=AUTH_ENDPOINT,
                            endpoint_url=COS_ENDPOINT, # Add the S3 endpoint URL
                            config=Config(signature_version='s3v4'))
