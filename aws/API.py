import boto3


class API:
    def __init__(self):
        self.clientEC2 = boto3.client('ec2')
        self.clientASG = boto3.client('autoscaling')

    '''Get all ec2 instances description and return an array of InstanceId'''
    def describeInstances(self):
        response = self.clientEC2.describe_instances()["Reservations"]
        instancesId = []
        for instance in response:
            info = instance["Instances"][0]
            instancesId.append(info["InstanceId"])
        return instancesId

    '''Get all auto-scaling groups description and return an array of AutoScalingGroupName'''
    def describeAutoScalingGroups(self):
        response = self.clientASG.describe_auto_scaling_groups()['AutoScalingGroups']
        groupNames = []
        for group in response:
            groupNames.append(group["AutoScalingGroupName"])
        return groupNames
