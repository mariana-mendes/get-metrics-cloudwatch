import boto3


class API:
    def __init__(self):
        self.clientEC2 = boto3.client('ec2')

    def describeInstances():
        response = clientEC2.describe_instances()
        for instance in response:
            print(response)
