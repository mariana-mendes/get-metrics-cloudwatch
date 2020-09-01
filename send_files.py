#!/usr/bin/env python3

from datetime import date
from log.setup import setup_log
import boto3

client = boto3.client('s3')
logger = setup_log()

logger.info('Initializing transfer data to s3 bucket')

today_file = date.today().strftime("%Y-%m-%d")

response = client.put_object(
    Body=(open('./'+today_file+'.csv', 'rb')),
    Bucket='log-ec2-instance',
    Key=today_file,
)
print(response['ResponseMetadata']['HTTPStatusCode'])
