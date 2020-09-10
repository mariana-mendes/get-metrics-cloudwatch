import boto3


class API:
    def __init__(self):
        self.clientEC2 = boto3.client('ec2')
        self.clientASG = boto3.client('autoscaling')
        self.clientELB = boto3.client('elbv2')

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
        response = self.clientASG.describe_auto_scaling_groups(
        )['AutoScalingGroups']
        groupNames = []
        for group in response:
            groupNames.append(group["AutoScalingGroupName"])
        return groupNames

    '''Get all load balancers description and return an array of LoadBalancerName'''

    def describeLoadBalancers(self):
        response = self.clientELB.describe_load_balancers()['LoadBalancers']
        elbNames = []
        for lb in response:
            stringLB = lb['LoadBalancerArn'].split(':')[-1].split(
                "loadbalancer/")[-1]
            elbNames.append(stringLB)
        return elbNames
