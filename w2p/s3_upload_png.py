import numpy as np
import pandas as pd
import os
from helpers.visualize import chart_curves
from definitions import PROCESSED_DATA_DIR,PROCESSED_DATA_CATALOG,PNG_FOLDER, S3_BUCKET, S3_FOLDER
import time
import boto3

def s3_ls(bucket,folder):
    session = boto3.Session(profile_name='default')
    s3 = session.client('s3')
    for key in s3.list_objects(Bucket=bucket)['Contents']:
        print(key['Key'])

png_list=os.listdir(PNG_FOLDER)
#print(png_list)

bucket=S3_BUCKET
folder=S3_FOLDER

session = boto3.Session(profile_name='default')
s3=session.client('s3')

s3_ls(bucket,folder)
i=0
start_time=time.time()

for png in png_list:
    s3_path = os.path.join(S3_FOLDER, png)
    local_path=os.path.join(PNG_FOLDER,png)
    print('Uploading:',i,png)
    s3.upload_file(local_path, bucket, s3_path,ExtraArgs={'ACL':'public-read'})
    execution_time = (time.time() - start_time)
    print('Time in minutes:',execution_time/60 )
    extrapolated_time=(len(png_list)/(i+1))*execution_time
    print('Time extrapolated to full TCE file (hours):',extrapolated_time/3600)
    print('Time remaining (hours):',(extrapolated_time-execution_time)/3600)
    i+=1


s3_ls(bucket,folder)

