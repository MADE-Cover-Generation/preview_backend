import os

from dotenv import load_dotenv

import boto3

class Uploader():
    def __init__(self):

        load_dotenv()
        self.client = boto3.client(
            's3',
	        endpoint_url = os.getenv('endpoint_url'),
	        aws_access_key_id = os.getenv('aws_access_key_id'),
	        aws_secret_access_key = os.getenv('aws_secret_access_key')
        )


    def upload(self, file_path, type = "previews"):
        result = self.__upload(type, file_path)
        return result

	
    def __upload(self, type, file_path: str) -> str:
        if type == 'previews':
            bucket = os.getenv('bucket_name_previews')
        else:
            bucket = os.getenv('bucket_name_summaries')
        print(bucket)
        object_name = os.path.basename(file_path)
        try:
            response = self.client.upload_file(file_path, bucket, object_name)
        except Exception as e:
            print(e)
            return None
        return object_name

