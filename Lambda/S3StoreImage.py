import json
import base64
import boto3
import os
import logging
from datetime import datetime

logging.basicConfig(level=logging.INFO)

def lambda_handler(event, context):
    method = event['requestContext']['http']['method']
    if method == 'GET':
        return {'statusCode': 200, 'body': json.dumps('GET Request received') }
    elif method == 'POST':
        try:
            bucket_name = os.environ['BUCKET_NAME']
        except:
            return {'statusCode': 500, 'body': "Unable to load required environment configuraiton" }
        try:
            image_bytes = base64.b64decode(event['body'])
            content_length = event['headers']['content-length']
            image_bytes = b"\xFF" + image_bytes
            dt = datetime.strftime(datetime.now(), "%Y-%d-%m_%H")
            file_name = dt + ".jpg"
            s3 = boto3.resource('s3')
            s3.Bucket(bucket_name).put_object(Key=file_name, Body=image_bytes)
        except Exception as err:
            logging.error(f"Execution failed due to error: {err}")
            return {'statusCode': 500, 'body': 'Internal Server Error' }
        
        return {'statusCode': 200, 'body': "Success" }
    else:
        return {'statusCode': 404, 'body': json.dumps('Requested resource not found.') }
