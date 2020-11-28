import constants as cons
import boto3
from botocore import exceptions
import dateutil.parser
import datetime
from dateutil.tz import tzlocal
from process_data.process import joinMetrics, saveRawFile, processASGFiles
from log.setup import setup_log
import json
from aws.API import API as api
import numpy as np


class CollectorAgent:
    def __init__(self, metrics, start, end, period, storage, awsconfig):
        self.metrics = metrics
        self.start = start
        self.end = end
        self.period = period
        self.client = boto3.client('cloudwatch', awsconfig["region"])
        self.logger = setup_log()
        self.storage = storage
        self.api = api()

    ''' For each metric registered in config.json (metricsDescription) call retrieveFromCloudWatch'''
    def getMetrics(self):
        for metric in self.metrics:
            self.retrieveFromCloudWatch(metric)

    ''' With the metric name and the dimension (id, name, unique value, etc), 
       retrieve the metric from CloudWatch for each dimension value'''
    def retrieveFromCloudWatch(self, metric):
        metricDimension = metric[cons.DIMENSION_KEY]
        valuesDimension = self.getDimensionValues(metric[cons.DIMENSION_KEY])

        for value in valuesDimension:
            try:
                response = self.client.get_metric_statistics(
                    Namespace=metric[cons.NAMESPACE_KEY],
                    MetricName=metric[cons.METRIC_NAME_KEY],
                    Dimensions=[
                        {
                            "Name": metricDimension,
                            "Value": self.getValueId(metricDimension, value)
                        },
                    ],
                    StartTime=dateutil.parser.isoparse(self.start),
                    EndTime=dateutil.parser.isoparse(self.end),
                    Period=int(self.period),
                    Statistics=metric[cons.STATISTICS_KEY],
                )
                joinMetrics(response, metric, value, self.storage[metricDimension])

            except exceptions.ClientError as error:
                self.logger.error(error)


    def getValueId(self, metricDimension, value):
        if(metricDimension == "LoadBalancer"):
            return self._getLoadBalancerName(value)
        else:
            return value[metricDimension]


    ''' Return list of values (ids, unique names, etc) from a specific dimension.'''
    def getDimensionValues(self, dimension):
        values = []
        if (dimension == cons.INSTANCE_ID_KEY):
            values =  self.api.describeInstances()
        elif(dimension == cons.AUTOSCALINGGROUP_ID_KEY):
            values =  self.api.describeAutoScalingGroups()
        elif(dimension == "LoadBalancer"):
            values =   self.api.describeLoadBalancers()
        return values

    def _getLoadBalancerName(self, lb):
        stringLB = lb["LoadBalancerArn"].split(':')[-1].split(
                "loadbalancer/")[-1]
        return stringLB

    def getDescriptionsASG(self):
        try:
            response = self.api.describeAutoScalingGroups()
            processASGFiles(response)
        except Exception as e:
           self.logger.error('Error trying to get autoscaling group descriptions')

    def getEventsASG(self):
        try:
            response = self.api.getScalingActivities()
            saveRawFile(response)
        except Exception as e:
           self.logger.error('Error trying to get autoscaling group activities')

