import ibm_boto3
from ibm_botocore.client import Config
# IBM Cloud credentials
API_KEY = 'your_api_key'
SERVICE_INSTANCE_ID = 'your_service_instance_id'
ENDPOINT = 'your_endpoint_url'
# Create IBM Cloud client
cos = ibm_boto3.client('s3',
                        ibm_api_key_id=API_KEY,
                        ibm_service_instance_id=SERVICE_INSTANCE_ID,
                        ibm_auth_endpoint=ENDPOINT,
                        config=Config(signature_version='s3v4'))

