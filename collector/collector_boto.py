import os
from string import Template
import constants as cons
import boto3
import dateutil.parser
import datetime
from dateutil.tz import tzlocal
from process_data.process import joinMetrics
import pandas as pd
import json


class CollectorAgentWithBoto:
    def __init__(self, metrics, instanceDescription, start, end, period):
        self.metrics = metrics
        self.instanceDescription = instanceDescription
        self.start = start
        self.end = end
        self.period = period

    def getMetrics(self):
        client = boto3.client('cloudwatch')
        metricsList = []
        for metric in self.metrics:
            for instance in self.instanceDescription:
                response = client.get_metric_statistics(
                    Namespace=metric['namespace'],
                    MetricName=metric['metricName'],
                    Dimensions=[
                        {
                            "Name": "InstanceId",
                            "Value": instance[0]['id']
                        },
                    ],
                    StartTime=dateutil.parser.isoparse(self.start),
                    EndTime=dateutil.parser.isoparse(self.end),
                    Period=int(self.period),
                    Statistics=['Average', 'Minimum', 'Maximum'],
                )
                # teste = {'Label': 'CPUUtilization', 'Datapoints': [{'Timestamp': datetime.datetime(2020, 8, 25, 19, 16, tzinfo=tzlocal()), 'Average': 0.0994720755765506, 'Minimum': 0.0, 'Maximum': 0.169491525423731, 'Unit': 'Percent'}, {'Timestamp': datetime.datetime(2020, 8, 25, 19, 51, tzinfo=tzlocal()), 'Average': 0.06723163841808, 'Minimum': 0.0, 'Maximum': 0.169491525423731, 'Unit': 'Percent'}, {'Timestamp': datetime.datetime(2020, 8, 25, 19, 21, tzinfo=tzlocal()), 'Average': 0.0666666666666652, 'Minimum': 0.0, 'Maximum': 0.166666666666669, 'Unit': 'Percent'}, {'Timestamp': datetime.datetime(2020, 8, 25, 19, 56, tzinfo=tzlocal()), 'Average': 0.0994535519125674, 'Minimum': 0.0, 'Maximum': 0.166666666666669, 'Unit': 'Percent'}, {'Timestamp': datetime.datetime(2020, 8, 25, 19, 6, tzinfo=tzlocal()), 'Average': 0.1000000000000014, 'Minimum': 0.0, 'Maximum': 0.166666666666669, 'Unit': 'Percent'}, {'Timestamp': datetime.datetime(2020, 8, 25, 19, 41, tzinfo=tzlocal()), 'Average': 0.0666666666666676, 'Minimum': 0.0, 'Maximum': 0.166666666666669, 'Unit': 'Percent'}, {'Timestamp': datetime.datetime(2020, 8, 25, 19, 11, tzinfo=tzlocal(
                # )), 'Average': 0.0338983050847438, 'Minimum': 0.0, 'Maximum': 0.169491525423719, 'Unit': 'Percent'}, {'Timestamp': datetime.datetime(2020, 8, 25, 19, 46, tzinfo=tzlocal()), 'Average': 0.0666666666666652, 'Minimum': 0.0, 'Maximum': 0.166666666666669, 'Unit': 'Percent'}, {'Timestamp': datetime.datetime(2020, 8, 25, 19, 31, tzinfo=tzlocal()), 'Average': 0.0661202185792336, 'Minimum': 0.0, 'Maximum': 0.166666666666669, 'Unit': 'Percent'}, {'Timestamp': datetime.datetime(2020, 8, 25, 19, 36, tzinfo=tzlocal()), 'Average': 0.066120218579236, 'Minimum': 0.0, 'Maximum': 0.166666666666669, 'Unit': 'Percent'}, {'Timestamp': datetime.datetime(2020, 8, 25, 19, 26, tzinfo=tzlocal()), 'Average': 0.09890710382513819, 'Minimum': 0.0, 'Maximum': 0.166666666666669, 'Unit': 'Percent'}], 'ResponseMetadata': {'RequestId': 'b86b8b4d-42e0-46a8-8478-acca7cec0fc7', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'b86b8b4d-42e0-46a8-8478-acca7cec0fc7', 'content-type': 'text/xml', 'content-length': '2926', 'vary': 'accept-encoding', 'date': 'Tue, 25 Aug 2020 20:06:28 GMT'}, 'RetryAttempts': 0}}
                joinMetrics(response, instance[0]['id'], metric['metricName'])
