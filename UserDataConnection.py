class UserDataConnector:
    def __init__(self, username):
        self.username = username
    def connect_to_data(self):
        # Get user bucket name (e.g., username-data)
        bucket_name = f'{self.username}-data'
        # List user objects (files/data) in bucket
        objects = cos.list_objects(Bucket=bucket_name)
        # Return object keys (file names) for user data
        return [obj['Key'] for obj in objects['Contents']
    def get_data(self, object_key):
        # Get object (file/data) from bucket
        obj = cos.get_object(Bucket=f'{self.username}-data', Key=object_key)
        # Return object body (file/data content)
        return obj['Body'].read()
# Example usage:
connector = UserDataConnector('john_doe')
user_data_files = connector.connect_to_data()
print(user_data_files)
# Get specific data file content
data_content = connector.get_data('user_profile.json')
print(data_content)
