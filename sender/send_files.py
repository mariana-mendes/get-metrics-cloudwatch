from datetime import date
from log.setup import setup_log
import boto3
import constants as cons
import tarfile
import os


class Sender:
    def __init__(self):
        self.logger = setup_log()
        self.client = boto3.client('s3')
        self.buckets = self.client.list_buckets()['Buckets']

    def compress_file(self, fileName, pathName):
        os.chdir(pathName)
        fileNameBase = os.path.splitext(fileName)[0] + ".tar.gz"
        with tarfile.open(fileNameBase, 'w:gz') as newFile:
            newFile.add(pathName + "/" + fileName,
                        arcname=fileName, recursive=False)

    def send_files(self):
        self.logger.info(cons.STARTING_SEND_FILES)
        originalDir = os.getcwd()
        dirData = os.getcwd() + "/data/"

        try:
            for folderName, subfolders, filenames in os.walk(dirData):
                for filename in filenames:
                    filePath = os.path.join(folderName, filename)
                    if filename.endswith(".csv"):
                        folderS3 = folderName.split("/")[-1])
                        fileNameBase=os.path.splitext(
                            filename)[0] + ".tar.gz"
                        self.compress_file(filename, folderName)
                        self.client.upload_file(
                            folderName + "/"+fileNameBase, 'log-ec2-instance', '%s/%s' % (folderS3, fileNameBase))
            os.chdir(originalDir)
        except Exception as e:
            self.logger.error(
                "Something went wrong trying to send files: %s", e.__class__)
            response={'ResponseMetadata': {'HTTPStatusCode': 404}}

        self.logger.info("Finishing data send to s3 bucket.")
