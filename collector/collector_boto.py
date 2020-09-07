import constants as cons
import boto3
import dateutil.parser
import datetime
from dateutil.tz import tzlocal
from process_data.process import joinMetricsEC2, joinMetricsASG
from log.setup import setup_log
import json


class CollectorAgentWithBoto:
    def __init__(self, metrics, instanceDescription, groupNames, start, end, period):
        self.metrics = metrics
        self.instanceDescription = instanceDescription
        self.groupNames = groupNames
        self.start = start
        self.end = end
        self.period = period
        self.client = boto3.client('cloudwatch', region_name=aws_region)
        self.logger = setup_log()

    def getMetrics(self):
        for metric in self.metrics:
            if(metric[cons.NAMESPACE_KEY] == "AWS/EC2"):
                self.getMetricsEC2(self, metric)
            elif(metric[cons.NAMESPACE_KEY] == "AWS/AutoScaling"):
                self.getMetricsAutoScaling(self, metric)

    def getMetricsEC2(self, metric):
            for instance in self.instanceDescription:
                try:
                    response = self.client.get_metric_statistics(
                        Namespace=metric[cons.NAMESPACE_KEY],
                        MetricName=metric[cons.METRIC_NAME_KEY],
                        Dimensions=[
                            {
                                "Name": cons.INSTANCE_ID_KEY,
                                "Value": instance[0]['id']
                            },
                        ],
                        StartTime=dateutil.parser.isoparse(self.start),
                        EndTime=dateutil.parser.isoparse(self.end),
                        Period=int(self.period),
                        Statistics=['Average', 'Minimum', 'Maximum'],
                    )
                    joinMetricsEC2(
                        response, instance[0]['id'], metric[cons.METRIC_NAME_KEY])

                except Exception as e:
                    self.logger.error('Something went wrong. Metric:  %s, Instance: %s, Error: %s',
                                      metric[cons.METRIC_NAME_KEY], instance[0]['id'], e.__class__)
        self.logger.info(cons.END_COLLECTOR)

    def getMetricsAutoScaling(self, metric):
            for groupName in self.groupNames:
                try:
                    response = self.client.get_metric_statistics(
                        Namespace=metric[cons.NAMESPACE_KEY],
                        MetricName=metric[cons.METRIC_NAME_KEY],
                        Dimensions=[
                            {
                                "Name": cons.AUTOSCALINGGROUP_ID_KEY,
                                "Value": groupName
                            },
                        ],
                        StartTime=dateutil.parser.isoparse(self.start),
                        EndTime=dateutil.parser.isoparse(self.end),
                        Period=int(self.period),
                        Statistics=['Average', 'Minimum', 'Maximum'],
                    )

                    joinMetricsASG(
                        response, groupName, metric[cons.METRIC_NAME_KEY])

                except Exception as e:
                    self.logger.error('Something went wrong. Metric:  %s, Group: %s, Error: %s',
                                 metric[cons.METRIC_NAME_KEY],groupName, e.__class__)
        self.logger.info(cons.END_COLLECTOR)
