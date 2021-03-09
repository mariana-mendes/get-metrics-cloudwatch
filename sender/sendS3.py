from datetime import date, datetime, timedelta
from log.setup import setup_log
import boto3
import constants as cons
import os
import tarfile

class SendS3:
    def __init__(self, awsconfig):
        self.logger = setup_log()
        self.client = boto3.client('s3', awsconfig['region'])
        self.buckets = self.client.list_buckets()['Buckets']
        self.bucket = awsconfig["bucket"]
        self.s3 = boto3.resource('s3')

    def bucketExists(self):
       return not self.s3.Bucket(self.bucket).creation_date is None 

    def send_folder(self, folder):
        self.logger.info(cons.STARTING_SEND_FILES)
        parentPath = os.getcwd()
        if(folder[len(folder)-1] == '/'):
            folder = folder[:-1] 
        folderName = folder.split("/")[-1]
        zipName = folderName + ".zip"
        folderS3 = folderName + "/" + zipName
        
        try:
            with tarfile.open(zipName, "w:gz") as tar:
                tar.add(parentPath + folder, arcname=os.path.basename(folderName))
            if(self.bucketExists()):
                response = self.client.upload_file(zipName, self.bucket, folderS3)
                os.remove(zipName)
            else: 
                self.logger.error("Unsend folder - Bucket {} doesn't existis".format(self.bucket))
        except Exception as e:
            self.logger.error(cons.ERROR_SEND_ZIP.format(e.__class__))

        self.logger.info("Finishing data send to s3 bucket.")

