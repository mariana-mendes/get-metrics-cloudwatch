import constants as cons
import boto3
import dateutil.parser
import datetime
from dateutil.tz import tzlocal
from process_data.process import joinMetrics
from log.setup import setup_log
import json


class CollectorAgent:
    def __init__(self, metrics, dimensionsValues, start, end, period, storage):
        self.metrics = metrics
        self.dimensionsValues = dimensionsValues
        self.start = start
        self.end = end
        self.period = period
        self.client = boto3.client('cloudwatch')
        self.logger = setup_log()
        self.storage = storage

    def getMetrics(self):
        for metric in self.metrics:
            self.retrieveFromCloudWatch(metric)

    def retrieveFromCloudWatch(self, metric):
        metricDimension = metric["dimension"]
        valuesDimension = self.dimensionsValues[metricDimension]

        for value in valuesDimension:
            try:
                response = self.client.get_metric_statistics(
                    Namespace=metric[cons.NAMESPACE_KEY],
                    MetricName=metric[cons.METRIC_NAME_KEY],
                    Dimensions=[
                        {
                            "Name": metricDimension,
                            "Value": value[metricDimension]
                        },
                    ],
                    StartTime=dateutil.parser.isoparse(self.start),
                    EndTime=dateutil.parser.isoparse(self.end),
                    Period=int(self.period),
                    Statistics=['Average', 'Minimum', 'Maximum'],
                )

                joinMetrics(
                    response, metric, metricDimension, value, self.storage[metricDimension])

            except Exception as e:
                self.logger.error('Something went wrong. Metric:  %s, Value: %s, Error: %s',
                                  metric[cons.METRIC_NAME_KEY], value, e.__class__)
        self.logger.info(cons.END_COLLECTOR)
