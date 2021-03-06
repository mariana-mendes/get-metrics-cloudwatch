import boto3


class API:
    def __init__(self, region):
        self.clientEC2 = boto3.client('ec2', region)
        self.clientASG = boto3.client('autoscaling',region)
        self.clientELB = boto3.client('elbv2',region)
        self.clientELBClassic = boto3.client('elb', region)


    '''Get all ec2 instances description and return an array of InstanceId'''

    def describeInstances(self):
        response = self.clientEC2.describe_instances()["Reservations"]
        return map(lambda instanceInfo: instanceInfo["Instances"][0], response)
     
    '''Get all auto-scaling groups description and return an array of AutoScalingGroupName'''
    def describeAutoScalingGroups(self):
        paginator = self.clientASG.get_paginator('describe_auto_scaling_groups')
        return paginator.paginate().build_full_result()

    
    '''Get all load balancers description and return'''
    def describeLoadBalancers(self):
        return self.clientELB.describe_load_balancers()['LoadBalancers']

    '''Get all load balancers description and return'''
    def describeLoadBalancersClassic(self):
        return self.clientELBClassic.describe_load_balancers()['LoadBalancerDescriptions']    
    
    def getScalingActivities(self):
        paginator = self.clientASG.get_paginator('describe_scaling_activities')
        return paginator.paginate(PaginationConfig={'MaxItems': 3000}).build_full_result()
        # return self.clientASG.describe_scaling_activities()



