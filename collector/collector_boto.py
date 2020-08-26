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
                joinMetrics(response, instance[0]['id'], metric['metricName'])
