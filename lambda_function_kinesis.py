import boto3
import json
import uuid
import random
import time
from faker import Faker
from datetime import datetime
import os

#setup
fake = Faker()
kinesis = boto3.client('kinesis', region_name='us-east-2')
stream_name = os.environ.get("STREAM_NAME", "clickstream-data") #change the name as per your setup

def generate_event():
    return {
        "user_id": f"u{random.randint(1000, 9999)}",
        "session_id": str(uuid.uuid4()),
        "event_time": datetime.utcnow().isoformat(),
        "event_type": random.choice(["pageview", "click", "add_to_cart", "checkout"]),
        "page_url": random.choice(["/home", "/products", "/product/42", "/cart"]),
        "referrer_url": random.choice(["/home", "/search", "/recommendations"]),
        "device_type": random.choice(["mobile", "desktop", "tablet"]),
        "browser": random.choice(["Chrome", "Safari", "Firefox"]),
        "geo": {
            "ip": fake.ipv4(),
            "country": fake.country_code(),
            "city": fake.city()
        }
    }

def lambda_handler(event, context):
    event_count = int(os.environ.get("RECORD_COUNT", "20")) #i simulated only 20 records but you can change it to however many
    
    for _ in range(event_count):
        event_data = generate_event()
        kinesis.put_record(
            StreamName=stream_name,
            Data=json.dumps(event_data),
            PartitionKey=event_data["user_id"]
        )
        time.sleep(1)  #basic delay 

    return {
        "statusCode": 200,
        "body": f"{event_count} clickstream records sent to {stream_name}"
    }
