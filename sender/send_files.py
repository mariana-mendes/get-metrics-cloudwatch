from datetime import date, datetime, timedelta
from log.setup import setup_log
import boto3
import constants as cons
import tarfile
import os

class Sender:
    def __init__(self, awsconfig):
        self.logger = setup_log()
        self.client = boto3.client('s3', awsconfig['region'])
        self.buckets = self.client.list_buckets()['Buckets']
        self.bucket = awsconfig["bucket"]
        self.s3 = boto3.resource('s3')

    def compress_file(self, fileName, pathName):
        os.chdir(pathName)
        fileNameBase = os.path.splitext(fileName)[0] + ".tar.gz"
        with tarfile.open(fileNameBase, 'w:gz') as newFile:
            newFile.add(pathName + "/" + fileName,
                        arcname=fileName, recursive=False)

    def bucketExists(self):
       return not self.s3.Bucket(self.bucket).creation_date is None 

    def send_files(self):
        self.logger.info(cons.STARTING_SEND_FILES)
        originalDir = os.getcwd()
        dirData = os.getcwd() + "/data/"

        try:
            for folderName, subfolders, filenames in os.walk(dirData):
                    for filename in filenames:
                        filePath = os.path.join(folderName, filename)

                        if filename.endswith(".csv"):
                            folderS3 = folderName.split("/")[-1]
                            fileNameBase=os.path.splitext(
                                filename)[0] + ".tar.gz"
                            fileDay = os.path.splitext(filename)[0]
                            today = date.today().strftime("%Y-%m-%d")
                            yesterday = (datetime.today() - timedelta(days=1)).strftime("%Y-%m-%d")
                            self.compress_file(filename, folderName)

                            # To evict send files from all days
                            if(self.bucketExists() and (fileDay == today or fileDay == yesterday)):
                                response = self.client.upload_file(folderName + "/" + fileNameBase, self.bucket, folderS3+'/{}'.format(fileNameBase))
                            else: 
                                self.logger.error("Unsend files - Bucket {} doesn't existis".format(self.bucket))
            os.chdir(originalDir)
        except Exception as e:
            self.logger.error(cons.ERROR_SEND_FILES.format(e.__class__))
        self.logger.info("Finishing data send to s3 bucket.")
