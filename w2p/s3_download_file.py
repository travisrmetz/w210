import os
from definitions import S3_BUCKET,PROCESSED_DATA_DIR
import boto3

def s3_ls(bucket):
    session = boto3.Session(profile_name='default')
    s3 = session.client('s3')
    for key in s3.list_objects(Bucket=bucket)['Contents']:
        print(key['Key'])

TEST_DIR='test_data'
#files_to_upload=['processed_tce.csv']
#files_to_download=['processed_final.csv','tce_table.csv','processed_tce.csv','globalbinned_df.csv','localbinned_df.csv','failed_kepids.csv']
files_to_download=['processed_final.csv']

bucket=S3_BUCKET
session = boto3.Session(profile_name='default')
s3=session.client('s3')

for file in files_to_download:
    local_file=os.path.join(PROCESSED_DATA_DIR,file)
    s3.download_file(bucket,file,os.path.join(TEST_DIR,file))


s3_ls(bucket)