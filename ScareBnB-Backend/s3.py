
import logging
from re import S
import boto3 
from botocore.exceptions import ClientError 
from botocore.client import Config 
import os
from dotenv import load_dotenv 
import uuid

# from filestorage import store

load_dotenv()


# Replace with your info
DO_SPACES_KEY = os.environ["DO_ACCESS_KEY"]
DO_SPACES_SECRET = os.environ["DO_SECRET_KEY"]
DO_REGION = os.environ["DO_REGION"]  # or sgp1, fra1, etc.
DO_ENDPOINT = os.environ["DO_ENDPOINT_URL"]
DO_URL = os.environ["DO_URL"]
BUCKET = os.environ["BUCKET"]
FOLDER = os.environ["FOLDER"]

# Determine if S3 is configured                                                                                           
S3_CONFIGURED = bool(DO_SPACES_KEY and DO_SPACES_SECRET and DO_REGION and DO_ENDPOINT and BUCKET and FOLDER)              

s3 = None # Initialize s3 client as None                                                                                  
if S3_CONFIGURED:                                                                                                         
    session = boto3.session.Session()                                                                                     
    s3 = session.client(                                                                                                  
        's3',                                                                                                             
        region_name=DO_REGION,                                                                                            
        endpoint_url=DO_ENDPOINT,                                                                                         
        aws_access_key_id=DO_SPACES_KEY,                                                                                  
        aws_secret_access_key=DO_SPACES_SECRET,                                                                           
        config=Config(signature_version='s3v4')                                                                           
    )                                                                                                                     
    try:                                                                                                                  
        # Initial check to see if bucket is accessible                                                                    
        s3.list_objects_v2(Bucket=BUCKET, MaxKeys=1) # Check with MaxKeys=1 for efficiency                                
        print(f"✅ Successfully accessed S3 bucket '{BUCKET}'")                                                           
    except ClientError as e:                                                                                              
        print(f"❌ Error accessing S3 bucket '{BUCKET}': {e}. S3 operations might be impacted or use placeholders.")      
        # Optionally, you could force S3_CONFIGURED to False if this initial check fails                                  
        # S3_CONFIGURED = False                                                                                           
    except Exception as e:                                                                                                
        print(f"❌ Unexpected error during S3 client initialization or bucket check: {e}. S3 operations will likely use placeholders.")                                                                                                           
        S3_CONFIGURED = False # Treat as not configured if there's an unexpected error                                    
else:                                                                                                                     
    print("⚠️ S3 not configured due to missing environment variables. Using placeholders for S3 operations.")             
      


# session = boto3.session.Session()




# s3 = session.client(
#     's3',
#     region_name=DO_REGION,
#     endpoint_url=DO_ENDPOINT,
#     aws_access_key_id=DO_SPACES_KEY,
#     aws_secret_access_key=DO_SPACES_SECRET,
#     config=Config(signature_version='s3v4')
# )

# try:
#     response = s3.list_objects_v2(Bucket=BUCKET)
#     print(f"✅ Successfully accessed bucket '{BUCKET}'")
# except ClientError as e:
#     print("❌ Error accessing bucket:", e)


# BUCKET = os.environ["BUCKET"]
# FOLDER = os.environ["FOLDER"]
# print("bucket name", BUCKET)


def upload_file(file_name, bucket=BUCKET, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = f"{FOLDER}/"+str(uuid.uuid4())

    try:
        response = s3.upload_file(
            file_name,
            BUCKET,
            object_name,
            # ContentType="image/jpeg",
            # ACL='public-read'
        )

        print('response', response)
        image = f"{DO_URL}/{object_name}"
    except ClientError as e:
        print('Image did not upload')
        logging.error(e)
        return False
    print('image', image, 'object_name', object_name)
    return [image, object_name]


def get_images(bucket=BUCKET):

    image_urls = []
    try:
        for item in s3.list_objects(Bucket=BUCKET, Prefix=FOLDER)["Contents"]:
            presigned_url = s3.generate_presigned_url(
                "get_object", Params={"Bucket": BUCKET, "Key": item["Key"]}
            )
            image_urls.append(presigned_url)
    except Exception as e:
        print(f"errors: {e}")
        logging.error(e)
      
    return image_urls[1:]

get_images(BUCKET)
