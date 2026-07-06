import logging

import boto3
from botocore.exceptions import ClientError

logger = logging.getLogger(__name__)

def create_bucket(bucket_name : str, region = 'us-east-1') -> bool:
    s3_client = boto3.client('s3',region_name=region)
    bucket_list = [i['Name'] for i in s3_client.list_buckets()['Buckets']]
    if bucket_name in bucket_list:
        logger.warning("Bucket %s already exists", bucket_name)
        return False
    else:
        try:
            s3_client.create_bucket(Bucket=bucket_name)
            return True
        except ClientError as e:
            logger.error("Bucket not created because of %s", e)
            return False

def upload_to_bucket(file_path : str, bucket_name : str, object_name : str, region = 'us-east-1') -> bool:
    s3_client = boto3.client('s3',region_name=region)
    try:
        s3_client.upload_file(file_path, bucket_name, object_name)
    except ClientError as e:
        logger.error("File not uploaded because of %s", e)
        return False
    return True