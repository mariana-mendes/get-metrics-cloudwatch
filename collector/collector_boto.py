import constants as cons
import boto3
import dateutil.parser
import datetime
from dateutil.tz import tzlocal
from process_data.process import joinMetrics
from log.setup import setup_log
import json


class CollectorAgentWithBoto:
    def __init__(self, metrics, instanceDescription, start, end, period):
        self.metrics = metrics
        self.instanceDescription = instanceDescription
        self.start = start
        self.end = end
        self.period = period

    def getMetrics(self):
        logger = setup_log()

        try:
            client = boto3.client('cloudwatch')
            metricsList = []
        except Exception as e:
            logger.error(
                cons.ERROR_BOTO_CONNECTION, e.__class__)

        for metric in self.metrics:
            for instance in self.instanceDescription:
                try:
                    response = client.get_metric_statistics(
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

                    joinMetrics(
                        response, instance[0]['id'], metric[cons.METRIC_NAME_KEY])

                except Exception as e:
                    logger.error('Something went wrong. Metric:  %s, Instance: %s, Error: %s',
                                 metric[cons.METRIC_NAME_KEY], instance[0]['id'], e.__class__)
        logger.info(cons.END_COLLECTOR)
