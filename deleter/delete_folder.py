from datetime import date, datetime, timedelta
from log.setup import setup_log
import boto3
import constants as cons
import os

class deleteFolderS3:
    def __init__(self, awsconfig):
        self.logger = setup_log()
        self.client = boto3.client('s3', awsconfig['region'])
        self.buckets = self.client.list_buckets()['Buckets']
        self.bucket = awsconfig["bucket"]
        self.s3 = boto3.resource('s3')

    def bucketExists(self):
       return not self.s3.Bucket(self.bucket).creation_date is None 

    def delete_folder(self, folder):
        self.logger.info(cons.STARTING_SEND_FILES)
        if(folder[len(folder)-1] == '/'):
            folder = folder[:-1]
        
        folderToDelete = folder + '/' + folder + '.zip'

        try:
            if(self.bucketExists()):
                response = self.client.delete_object(Bucket=self.bucket, Key=folderToDelete)
            else: 
                self.logger.error("Bucket {} doesn't existis".format(self.bucket))
        except Exception as e:
            self.logger.error(cons.ERROR_DELETE_FOLDER.format(e.__class__))

        self.logger.info("Finishing data delete to s3 bucket.")

