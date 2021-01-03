
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
from moto import mock_cloudwatch
from moto.core import ACCOUNT_ID
import pandas as pd
import numpy as np


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

instanceMock = [{"InstanceId":"A"}]
instancesMock = [{"InstanceId":"A"}, {"InstanceId":"B"}, {"InstanceId":"C"}]

# create a collector instance
collector = CWA(configJson[cons.METRICS_KEY],  configJson[cons.START_TIME_KEY],  configJson[cons.END_TIME_KEY], configJson[cons.PERIOD_KEY], configJson[cons.STORAGE], configJson[cons.AWS_CONFIG])

# put the metrics you want to retrieve
@mock_cloudwatch
def put_metric_data(conn):

    conn.put_metric_data(
        Namespace="AWS/Test",
        MetricData=[
            dict(
                MetricName="metric",
                Dimensions=[{"Name": "InstanceId", "Value": "i-092381023"}],
                Value=1.5,
                Timestamp=utc_now,
            )
        ],
    )

def put_metric_data_multiple_instances(conn, instances):
    values = [1, 2, 4]
    for i in range(len(instances)):
        conn.put_metric_data(
            Namespace="AWS/Test",
            MetricData=[
                dict(
                    MetricName="metric",
                    Dimensions=[{"Name": "InstanceId", "Value": instances[i]["InstanceId"]}],
                    Value=values[i],
                    Timestamp=utc_now,
                )
            ],
        )
    

@mock_cloudwatch
def test_get_metric_statistics():
    conn = boto3.client("cloudwatch", region_name="us-east-1")

    put_metric_data(conn)
    stats = conn.get_metric_statistics(
        Namespace="AWS/Test",
        MetricName="metric",
        StartTime=utc_now - timedelta(seconds=60),
        EndTime=utc_now + timedelta(seconds=60),
        Period=60,
        Statistics=["SampleCount", "Sum"],
    )


    all_metric_data = collector.retrieveFromCloudWatch(configJson[cons.METRICS_KEY][0], instanceMock)
    col = ['timestamp', 'InstanceId', 'metricName', 'SampleCount', 'Sum']
    newDf = pd.DataFrame(data=all_metric_data, columns = col)

    datapoint = stats["Datapoints"][0]
    sumIsEqual = np.allclose( newDf['Sum'][0],  datapoint["Sum"])
    sampleCountIsEqual = np.allclose(newDf['SampleCount'][0],  datapoint["SampleCount"])
   

    # Testing results
    sumIsEqual.should.be.true
    sampleCountIsEqual.should.be.true
    stats["Datapoints"].should.have.length_of(len(all_metric_data))


@mock_cloudwatch
def test_get_metric_statistics_multiple_instances():
    conn = boto3.client("cloudwatch", region_name="us-east-1")
    put_metric_data_multiple_instances(conn, instancesMock)

    # TO-DO: Implement this test when this issue is done: 
    # https://github.com/spulec/moto/blob/master/moto/cloudwatch/responses.py#L152

#     stats = conn.get_metric_statistics(
#                     Namespace="AWS/Test",
#                     MetricName="metric",
#                     Dimensions=[
#                         {
#                             "Name": "InstanceId",
#                             "Value": "A"
#                         },
#                     ],
#                     StartTime=utc_now - timedelta(seconds=60),
#                     EndTime=utc_now + timedelta(seconds=60),
#                     Period=60,
#                     Statistics=["SampleCount", "Sum", "Maximum", "Minimum"],
# )



test_get_metric_statistics()