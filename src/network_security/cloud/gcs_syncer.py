import os 
from google.cloud import storage

class GSCSync:
    def __init__(self):
        self.client = storage.Client()
        
    def sync_folder_to_gcs(self, folder, bucket_name, gcs_prefix):
        bucket = self.client.bucket(bucket_name)
        
        for root, dirs, files in os.walk(folder):
            for file in files:
                local_path = os.path.join(root, file)
                relative_path = os.path.relpath(local_path, folder)
                gcs_path = f"{gcs_prefix}/{relative_path}".replace("\\", "/")
                
                blob = bucket.blob(gcs_path)
                blob.upload_from_filename(local_path)
                print(f"Uploaded: {local_path} → gs://{bucket_name}/{gcs_path}")
    
    def sync_folder_from_gcs(self, folder, bucket_name, gcs_prefix):
        bucket = self.client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=gcs_prefix)
        
        for blob in blobs:
            relative_path = os.path.relpath(blob.name, gcs_prefix)
            local_path = os.path.join(folder, relative_path)
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            
            blob.download_to_filename(local_path)
            print(f"Downloaded: gs://{bucket_name}/{blob.name} → {local_path}")