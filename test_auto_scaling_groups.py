
import boto3
from botocore.exceptions import ClientError
from datetime import datetime, timedelta
import dateutil.parser
import pytest
from uuid import uuid4
import pytz
import sure
import constants as cons
from collector.collector_boto import CollectorAgent as CWA
from moto.core import ACCOUNT_ID
import pandas as pd
import numpy as np

from moto import (
    mock_cloudwatch,
    mock_autoscaling,
    mock_ec2_deprecated,
    mock_elb_deprecated,
    mock_elb,
    mock_autoscaling_deprecated,
    mock_ec2,
    mock_cloudformation,
)

# pre-config
utc_now = datetime.now(tz=pytz.utc)
configJson = {
    "metricsDescription": [
        {
            "metricName": "metric",
            "namespace": "AWS/Test",
            "dimension": "InstanceId",
            "statistics": ["SampleCount", "Sum"]
        }
    ],
    "endTime": (utc_now + timedelta(seconds=60)).isoformat(),
    "period": "60",
    "startTime": (utc_now - timedelta(seconds=60)).isoformat(),
    "storage": {},
    "aws-config": {
        "region": "us-east-1",
    }
}

collector = CWA(configJson[cons.METRICS_KEY],  configJson[cons.START_TIME_KEY],  configJson[cons.END_TIME_KEY], configJson[cons.PERIOD_KEY], configJson[cons.STORAGE], configJson[cons.AWS_CONFIG])

# collector.getDescriptionsASG()

@mock_ec2
def setup_networking():
    ec2 = boto3.resource("ec2", region_name="us-east-1")
    vpc = ec2.create_vpc(CidrBlock="10.11.0.0/16")
    subnet1 = ec2.create_subnet(
        VpcId=vpc.id, CidrBlock="10.11.1.0/24", AvailabilityZone="us-east-1a"
    )
    subnet2 = ec2.create_subnet(
        VpcId=vpc.id, CidrBlock="10.11.2.0/24", AvailabilityZone="us-east-1b"
    )
    return {"vpc": vpc.id, "subnet1": subnet1.id, "subnet2": subnet2.id}

@mock_autoscaling
def list_autoscaling_groups():
    mocked_networking = setup_networking()
    conn = boto3.client("autoscaling", region_name="us-east-1")
    conn.create_launch_configuration(LaunchConfigurationName="TestLC")

    for i in range(51):
        conn.create_auto_scaling_group(
            AutoScalingGroupName="TestGroup%d" % i,
            MinSize=1,
            MaxSize=2,
            LaunchConfigurationName="TestLC",
            VPCZoneIdentifier=mocked_networking["subnet1"],
        )
    
    response = conn.describe_auto_scaling_groups()
    groups = response["AutoScalingGroups"]
    all_metric_data = collector.getDescriptionsASG()
    (len(groups) == len(all_metric_data)).should.be.true

@mock_autoscaling
def format_file_ASG():
    mocked_networking = setup_networking()
    conn = boto3.client("autoscaling", region_name="us-east-1")
    conn.create_launch_configuration(LaunchConfigurationName="TestLC")

    for i in range(10):
        conn.create_auto_scaling_group(
            AutoScalingGroupName="TestGroup%d" % i,
            MinSize=1,
            MaxSize=2,
            LaunchConfigurationName="TestLC",
            VPCZoneIdentifier=mocked_networking["subnet1"],
        )
    
    all_metric_data = collector.getDescriptionsASG()
    (all_metric_data.columns.values.tolist() == ['timestamp','InstanceId','AutoscalingGroup']).should.be.true

@mock_autoscaling
def format_file_events_ASG():
    mocked_networking = setup_networking()
    conn = boto3.client("autoscaling", region_name="us-east-1")
    conn.create_launch_configuration(LaunchConfigurationName="TestLC")

    for i in range(10):
        conn.create_auto_scaling_group(
            AutoScalingGroupName="TestGroup%d" % i,
            MinSize=1,
            MaxSize=2,
            LaunchConfigurationName="TestLC",
            VPCZoneIdentifier=mocked_networking["subnet1"],
        )
    
    all_metric_data = collector.getEventsASG()
    print(all_metric_data)
    # (all_metric_data.columns.values.tolist() == ['ActivityId','AutoScalingGroupName','Description','Cause','StartTime','EndTime','StatusCode']).should.be.true





list_autoscaling_groups()
format_file_ASG()
format_file_events_ASG()