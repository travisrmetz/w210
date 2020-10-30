import numpy as np
import pandas as pd
import os
from definitions import S3_BUCKET,PROCESSED_DATA_DIR
import time
import boto3

def s3_ls(bucket):
    session = boto3.Session(profile_name='default')
    s3 = session.client('s3')
    for key in s3.list_objects(Bucket=bucket)['Contents']:
        print(key['Key'])


files_to_upload=['processed_tce.csv']

bucket=S3_BUCKET
session = boto3.Session(profile_name='default')
s3=session.client('s3')
for file in files_to_upload:
    local_file=os.path.join(PROCESSED_DATA_DIR,file)
    s3.upload_file(local_file, bucket, file,ExtraArgs={'ACL':'public-read'})


s3_ls(bucket)

