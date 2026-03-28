import os
from google.cloud import storage
from dotenv import load_dotenv
load_dotenv()

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
GOOGLE_BUCKET_NAME = os.getenv("GOOGLE_BUCKET_NAME")

client = storage.Client()
bucket = client.get_bucket(GOOGLE_BUCKET_NAME)
print(f"Connected! Bucket: {bucket.name}")