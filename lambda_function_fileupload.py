# lambda_function.py
import json
import base64
import boto3
import uuid
from datetime import datetime

s3 = boto3.client('s3')
bucket_name = ''  # replace with your actual bucket name

def lambda_handler(event, context):
    for record in event['Records']:
        # Decode base64 Kinesis record
        payload = base64.b64decode(record['kinesis']['data'])
        click_event = json.loads(payload)
        
        # Create unique file name with timestamp folder
        key = f"{datetime.today().strftime('%Y/%m/%d')}/{uuid.uuid4()}.json"
        
        # Upload to S3
        s3.put_object(Bucket=bucket_name, Key=key, Body=json.dumps(click_event))
    
    return {
        'statusCode': 200,
        'body': 'Processed records successfully'
    }
