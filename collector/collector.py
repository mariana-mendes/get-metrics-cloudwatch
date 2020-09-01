import os
from string import Template
import constants as cons
import boto3


class CollectorAgent:
    def __init__(self, metrics, instanceDescription, start, end, period):
        self.metrics = metrics
        self.instanceDescription = instanceDescription
        self.start = start
        self.end = end
        self.period = period

    def getAWSMetric(self, metric, instance):
        try:
            command = Template(cons.GET_METRIC_AWS)
            commandString = command.substitute(
                metric=metric['metricName'], idInstance=instance['id'], period=self.period, start=self.start, end=self.end, id=instance['id'])
            os.system(commandString)
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")

    def getCWAMetric(self, metric, instance):
        try:
            command = Template(cons.GET_METRIC_CWAGENT)
            commandString = command.substitute(metric=metric['metricName'], img=instance['img'], type=instance['type'],
                                               idInstance=instance['id'], period=self.period, start=self.start, end=self.end, id=instance['id'])
            os.system(commandString)
        except Exception as e:
            print("Oops!", e.__class__, "occurred.")

    def getMetrics(self):
        for metric in self.metrics:
            for instance in self.instanceDescription:
                if(metric['namespace'] == 'AWS/EC2'):
                    self.getAWSMetric(metric, instance[0])
                else:
                    self.getCWAMetric(metric, instance[0])
