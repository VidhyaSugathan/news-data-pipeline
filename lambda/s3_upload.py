import os
import boto3
from dotenv import load_dotenv
from botocore.exceptions import ClientError

load_dotenv()

s3 = boto3.client(
    "s3",
    region_name=os.getenv("AWS_REGION"),
)

file_path = "/tmp/news.json"

bucket_name = os.getenv("S3_BUCKET_NAME")


def upload_to_s3():
    try:
        s3.upload_file(file_path, bucket_name, "raw/news.json")
        print("File uploaded successfully!")

    except ClientError as e:
        print(f"AWS Error: {e}")

    except FileNotFoundError:
        print("news.json not found!")

    except Exception as e:
        print(f"Unexpected Error: {e}")
