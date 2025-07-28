from minio import Minio
from minio.error import S3Error
import os

# Load these from your .env.production file ideally
MINIO_ENDPOINT = "141.148.205.10:9000"  # Change if MinIO is remote
MINIO_ACCESS_KEY = "minioadmin"
MINIO_SECRET_KEY = "minioadmin123"
MINIO_BUCKET = "video-converter"

# Initialize the MinIO client
minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False  # Set to True if using https
)

# Create bucket if it doesn't exist
if not minio_client.bucket_exists(MINIO_BUCKET):
    minio_client.make_bucket(MINIO_BUCKET)

def upload_to_minio(local_file_path: str, object_name: str):
    try:
        minio_client.fput_object(
            MINIO_BUCKET,
            object_name,
            local_file_path,
        )
        print(f"Uploaded {object_name} to MinIO.")
    except S3Error as e:
        print("MinIO Upload Error:", e)
        raise

def download_from_minio(object_name: str, local_file_path: str):
    try:
        minio_client.fget_object(
            MINIO_BUCKET,
            object_name,
            local_file_path,
        )
        print(f"Downloaded {object_name} from MinIO.")
    except S3Error as e:
        print("MinIO Download Error:", e)
        raise
