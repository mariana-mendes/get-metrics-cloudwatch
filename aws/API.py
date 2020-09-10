import boto3


class API:
    def __init__(self):
        self.clientEC2 = boto3.client('ec2')

    def describeInstances(self):
        response = self.clientEC2.describe_instances()["Reservations"]
        instancesId = []
        for instance in response:
            info = instance["Instances"][0]
            instancesId.append(info["InstanceId"])
            # if "Tags" in info:
            #     print(info["Tags"])
      return instancesId
