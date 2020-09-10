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

    def compress_files(self):
        dirData = os.getcwd() + "/data/"
        for folder in os.listdir(dirData):
            pathName = dirData + folder
            for fileName in os.listdir(pathName):
                os.chdir(pathName)
                fileNameBase = os.path.splitext(fileName)[0]
                tar = tarfile.open(fileNameBase + ".tar.gz", mode="w:gz")
                tar.add(pathName + "/" + fileName,
                        arcname=fileName, recursive=False)
                tar.close()

    def send_files(self):
        self.logger.info(cons.STARTING_SEND_FILES)
        self.compress_files()
        try:
            dirData = os.getcwd() + "/data/"
            for folder in os.listdir(dirData):
                pathName = dirData + folder
                for fileName in os.listdir(pathName):
                    if fileName.endswith("tar.gz"):
                        response = self.client.put_object(
                            Body=(open(fileName, 'rb')),
                            Bucket='log-ec2-instance/log',
                            Key=self.file_to_send,
                        )
        except Exception as e:
            self.logger.error(
                "Something went wrong trying to send files: %s", e.__class__)
            response = {'ResponseMetadata': {'HTTPStatusCode': 404}}

        # self.logger.info("Finishing data send to s3 bucket. Status: %s",
        #                  response['ResponseMetadata']['HTTPStatusCode'])
