import boto3
import json
from process_data import processASGFiles, saveRawFile


class CollectorAgentASG:
    def __init__(self):
        self.client = boto3.client('autoscaling')

    def describeASG(self):
        try:
            response = self.client.describe_auto_scaling_groups()
            processASGFiles(response)
        except Exception as e:
            print(
                'Something went wrong while trying to describe autoscaling group'
            )

    def getHistoricEvents(self):
        try:
            response = self.client.describe_scaling_activities()
            saveRawFile(response)
        except Exception as e:
            print(
                'Something went wrong while trying to get scaling activities.')
