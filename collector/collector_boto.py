import os
from string import Template
import constants as cons
import boto3
import dateutil.parser

class CollectorAgentWithBoto:
  def __init__(self, metrics, instanceDescription, start, end, period):
    self.metrics = metrics
    self.instanceDescription = instanceDescription
    self.start = start
    self.end = end
    self.period = period


  def getMetrics(self):
    client = boto3.client('cloudwatch')
    for metric in self.metrics:
      for instance in self.instanceDescription:
        response = client.get_metric_statistics(
        Namespace=metric['namespace'],
        MetricName=metric['metricName'],
        Dimensions=[
            {
                "Name": "InstanceId",
                "Value": instance['id']
            },
        ],
        StartTime=dateutil.parser.isoparse(self.start),
        EndTime=dateutil.parser.isoparse(self.end),
        Period=self.period,
        Statistics=['Average','Minimum','Maximum' ],
    )




