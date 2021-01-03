
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

utc_now = datetime.now(tz=pytz.utc)
configJson = {
    "metricsDescription": [
        {
            "metricName": "metric",
            "namespace": "tester",
            "dimension": "InstanceId",
            "statistics": ["SampleCount", "Sum"]
        }
    ],
    "endTime": (utc_now + timedelta(seconds=60)).isoformat(),
    "period": "60",
    "startTime": (utc_now - timedelta(seconds=60)).isoformat(),
    "storage": {
        "InstanceId": "teste-1"
    },
    "aws-config": {
        "region": "us-east-1",
        "bucket": "jasjasjsaj"
    }
}


@mock_cloudwatch
def test_get_metric_statistics():
    conn = boto3.client("cloudwatch", region_name="us-east-1")
    collector = CWA(configJson[cons.METRICS_KEY],  configJson[cons.START_TIME_KEY],  configJson[cons.END_TIME_KEY], configJson[cons.PERIOD_KEY], configJson[cons.STORAGE], configJson[cons.AWS_CONFIG])

    ## Inserindo métrica
    conn.put_metric_data(
        Namespace="tester",
        MetricData=[
            dict(
                MetricName="metric",
                Dimensions=[{"Name": "InstanceId", "Value": "i-092381023"}],
                Value=1.5,
                Timestamp=utc_now,
            )
        ],
    )


    ## Recuperando métrica
    stats = conn.get_metric_statistics(
        Namespace="tester",
        MetricName="metric",
        StartTime=utc_now - timedelta(seconds=60),
        EndTime=utc_now + timedelta(seconds=60),
        Period=60,
        Statistics=["SampleCount", "Sum"],
    )

    all_metric_data = collector.retrieveFromCloudWatch(configJson[cons.METRICS_KEY][0], [{"InstanceId":"i-092381023"}])
    col = ['timestamp', 'InstanceId', 'metricName', 'SampleCount', 'Sum']
    newDf = pd.DataFrame(data=all_metric_data, columns = col)

    SampleCount = newDf['SampleCount'][0]
    Sum = newDf['Sum'][0]
    length_of = len(all_metric_data)

    datapoint = stats["Datapoints"][0]

    sumIsEqual = np.allclose(Sum,  datapoint["Sum"])
    sampleCountIsEqual = np.allclose(SampleCount,  datapoint["SampleCount"])
   

    sumIsEqual.should.be.true
    sampleCountIsEqual.should.be.true
    stats["Datapoints"].should.have.length_of(length_of)



test_get_metric_statistics()