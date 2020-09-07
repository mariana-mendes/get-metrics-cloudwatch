from datetime import date
from log.setup import setup_log
import boto3
import constants as cons
import tarfile
import os


class Sender:
    def __init__(self, file_to_send):
        self.logger = setup_log()
        self.client = boto3.client('s3')
        self.file_to_send = file_to_send

    def compress_file():
        tar = tarfile.open(self.file_to_send + ".tar.gz", mode="w:gz")
        tar.add(self.file_to_send, os.path.basename(self.file_to_send))
        tar.close()

    def send_files():
        self.logger.info(cons.STARTING_SEND_FILES)
        compress_file()
        try:
            response = self.client.put_object(
                Body=(open(self.file_to_send+'.tar.gz', 'rb')),
                Bucket='log-ec2-instance',
                Key=self.file_to_send,
            )
        except Exception as e:
            self.logger.error(
                "Something went wrong trying to send files: %s", e.__class__)
            response = {'ResponseMetadata': {'HTTPStatusCode': 404}}

        self.logger.info("Finishing data send to s3 bucket. Status: %s",
                         response['ResponseMetadata']['HTTPStatusCode'])
