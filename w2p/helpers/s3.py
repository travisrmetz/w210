import boto3
import os
import io
import pandas as pd
from botocore.exceptions import ClientError



#profile_name='afwerx' #this is config and credentials files in .aws
bucket='w210-project'
curve_folder='light_curve_png'
image_dir='processed_data\light_curve_png'

def get_s3_file(file_name,bucket=bucket, folder=folder,profile_name=profile_name):
    #Returns the data from an S3 file - no local file written
    session = boto3.Session(profile_name=profile_name)
    s3 = session.client('s3')
    path=os.path.join(folder,file_name)
    file_object=s3.get_object(Bucket=bucket,Key=path)
    file_content=file_object['Body'].read()
    file_content_bytes=io.BytesIO(file_content)
    return(file_content_bytes)

def put_csv_to_s3(dataframe,file_name,bucket=bucket,folder=folder,profile_name=profile_name):
    session = boto3.Session(profile_name=profile_name)
    s3 = session.client('s3')
    path = os.path.join(folder, file_name)
    csv_buffer=io.StringIO()
    dataframe.to_csv(csv_buffer,index=False)
    s3.put_object(Bucket=bucket,Key=path,Body=csv_buffer.getvalue(),
                  ServerSideEncryption='aws:kms')

def s3_ls(bucket=bucket,folder=folder,profile_name=profile_name):
    session = boto3.Session(profile_name=profile_name)
    s3 = session.client('s3')
    for key in s3.list_objects(Bucket=bucket)['Contents']:
        print(key['Key'])

def upload_file_to_s3(file_name,bucket=bucket,folder=folder,profile_name=profile_name):
    session = boto3.Session(profile_name=profile_name)
    s3 = session.client('s3')
    s3_path = os.path.join(folder, file_name)
    s3.upload_file(file_name, bucket, s3_path)

def load_data_from_file(file: str,bucket: str, raw_folder: str, profile_name: str,header:int) -> pd.DataFrame:
    """
    Load data from an excel file located in S3 into a dataframe.
    :param file: name of file
    :param bucket: name of S3 bucket
    :param raw_folder: name of folder within S3 bucket that has raw data
    :param profile_name: name of AWS profile to use for credentials
    :param header: number of rows before column headings
    :return: Dataframe containing the data
    """
    df=pd.read_excel(get_s3_file(file, bucket, raw_folder, profile_name), header=header)
    return df


def check_file(s3_client, bucket, key):
    '''
    checks if key already in bucket
    returns true if key already in bucket and false if not
    '''
    
    try:
        s3_client.head_object(Bucket=bucket, Key=key)
    except ClientError as e:
        return int(e.response['Error']['Code']) != 404
    return True


def upload_file(s3_client,file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3')
    try:
        response = s3_client.upload_file(file_name, bucket, object_name)
    except ClientError as e:
        logging.error(e)
        print ('File not uploaded:',object_name)
        return False
    print('File uploaded:',object_name)
    return True

#get list of files from image directory
file_list=os.listdir(image_dir)
print('# of files:',len(file_list))
s3_client=boto3.client('s3')

i=1
#cycle through files and upload to s3 bucket if not already there
for object_name in file_list:
    
    file_name=os.path.join(image_dir,object_name)
    
    print (i, object_name)
    i+=1
    
    #checks if file already there and uploads if not
    #note there is a little lag for S3 to register is there
    if not check_file(s3_client, bucket_name, file_name):
        #print(' not there')
        upload_file(s3_client,file_name,bucket_name,object_name)
    else:
        #print('there')
        print ('File already there:',file_name)