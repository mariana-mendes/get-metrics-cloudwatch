import logging
import boto3
from botocore.exceptions import ClientError

class Uploader:
    def __init__(self, aws_region):
        self.client = boto3.client('s3', region_name=aws_region)
        self.buckets = self.client.list_buckets()['Buckets']

    def alreadyExist(bucket):
        if not bucket in [dic['Name'] for dic in self.buckets]:
            print('There is no bucket named {bucket_name} in this account'.format(bucket_name=bucket))
            return True
        return False

    # TODO: mandar comprimido para S3 Glacier Deep Archive? Limitar os arquivos a varrer?
    def send2storage(self, folder_source, bucket, bucket_folder='', storage_class='STANDARD_IA'):
        if not os.path.exists(folder_source):
            print('Error while trying to find the folder file source:', folder_source)
            return False
        
        if not alreadyExist(bucket):
            return False
        
        for file_name in os.listdir(folder_source):
            # defining the S3 object name 
            if bucket_folder:
                object_name='{folder_name}/{file_name}'.format(folder_name=bucket_folder, file_name=file_name)
            else:
                object_name=file_name

            try:
                self.client.upload_file(file_name, bucket, object_name, ExtraArgs = {'StorageClass': storage_class})
            except ClientError as e:
                logging.error(e)
                return False
        return True