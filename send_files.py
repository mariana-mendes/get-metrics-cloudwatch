#!/usr/bin/env python3

from datetime import date
from log.setup import setup_log
import boto3
import constants as cons
import tarfile
import os


def compress_file():
    today_file = date.today().strftime("%Y-%m-%d")
    tar = tarfile.open(today_file + ".tar.gz", mode="w:gz")
    file_name = './'+today_file+'.csv'
    tar.add(file_name, os.path.basename(file_name))
    tar.close()


def send_file():
    logger = setup_log()
    logger.info(cons.STARTING_SEND_FILES)
    today_file = date.today().strftime("%Y-%m-%d")

    compress_file()
    try:
        client = boto3.client('s3')
        response = client.put_object(
            Body=(open('./'+today_file+'.tar.gz', 'rb')),
            Bucket='log-ec2-instance',
            Key=today_file,
        )
    except Exception as e:
        logger.error(
            "Something went wrong trying to send files: %s", e.__class__)
        response = {'ResponseMetadata': {'HTTPStatusCode': 404}}

    logger.info("Finishing data send to s3 bucket. Status: %s",
                response['ResponseMetadata']['HTTPStatusCode'])
