import ibm_boto3
from ibm_botocore.client import Config
# IBM Cloud credentials
API_KEY = 'your_api_key'
SERVICE_INSTANCE_ID = 'your_service_instance_id'
# --- IMPORTANT ---
# Replace 'your_api_key' and 'your_service_instance_id' with your actual credentials.
# Replace 'your_endpoint_url' with the correct IBM Cloud authentication endpoint,
# typically 'https://iam.cloud.ibm.com/identity/token'.
AUTH_ENDPOINT = 'https://iam.cloud.ibm.com/identity/token' # Common authentication endpoint

# Create IBM Cloud client
cos = ibm_boto3.client('s3',
                        ibm_api_key_id=API_KEY,
                        ibm_service_instance_id=SERVICE_INSTANCE_ID,
                        ibm_auth_endpoint=AUTH_ENDPOINT,
                        config=Config(signature_version='s3v4'))
