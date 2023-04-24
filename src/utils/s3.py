import os
import boto3


def download_s3_subdirectory(bucket_name, subdirectory, local_path):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    objects = bucket.objects.filter(Prefix=subdirectory)

    for obj in objects:
        if not os.path.exists(os.path.dirname(local_path + obj.key)):
            os.makedirs(os.path.dirname(local_path + obj.key))
        bucket.download_file(obj.key, local_path + obj.key)