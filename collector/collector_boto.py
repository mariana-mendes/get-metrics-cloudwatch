import constants as cons
import boto3
from botocore import exceptions
import dateutil.parser
import datetime
from dateutil.tz import tzlocal
from process_data.process import joinMetrics
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
        metricDimension = metric["dimension"]
        valuesDimension = self.getDimensionValues(metric["dimension"])
        values = np.array(valuesDimension)
        isObject =  values.dtype == object
        for value in values:
            try:
                response = self.client.get_metric_statistics(
                    Namespace=metric[cons.NAMESPACE_KEY],
                    MetricName=metric[cons.METRIC_NAME_KEY],
                    Dimensions=[
                        {
                            "Name": metricDimension,
                            "Value": self.getValueId(isObject, value)
                        },
                    ],
                    StartTime=dateutil.parser.isoparse(self.start),
                    EndTime=dateutil.parser.isoparse(self.end),
                    Period=int(self.period),
                    Statistics=['Average', 'Minimum', 'Maximum'],
                )
                joinMetrics(response, metric, metricDimension, value,
                            self.storage[metricDimension])
            except exceptions.ClientError as error:
                self.logger.error(error)


    def getValueId(self, isObject, value):
        if(isObject):
            return value["InstanceId"]
        else:
            return value


    ''' Return list of values (ids, unique names, etc) from a specific dimension.'''
    def getDimensionValues(self, dimension):
        values = []
        if (dimension == cons.INSTANCE_ID_KEY):
            values =  self.api.describeInstances()
        elif(dimension == cons.AUTOSCALINGGROUP_ID_KEY):
            values =  self.api.describeAutoScalingGroups()
        elif(dimension == cons.LOADBALANCER_ID_KEY):
            values =   self.api.describeLoadBalancers()
        return values
