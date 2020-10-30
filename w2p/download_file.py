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


PROCESSED_DATA_DIR='test_download_data'

#files_to_upload=['processed_tce.csv']
files_to_download=['tce_table.csv','processed_tce.csv','globalbinned_df.csv','localbinned_df.csv','failed_kepids.csv']

bucket=S3_BUCKET
session = boto3.Session(profile_name='default')
s3=session.client('s3')
for s3_file in files_to_download:
    local_file=os.path.join(PROCESSED_DATA_DIR,s3_file)
    print('local_file:',local_file)
    s3.download_file(bucket,s3_file,local_file)


s3_ls(bucket)