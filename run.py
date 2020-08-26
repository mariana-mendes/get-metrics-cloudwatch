#!/usr/bin/env python3

import os
import sys
import json
import constants as cons
import time
from datetime import datetime, timedelta
import boto3

from collector.collector import CollectorAgent as CW
from collector.collector_boto import CollectorAgentWithBoto as CWB


with open('config.json', 'r+') as f:
    data = json.load(f)
    # os.system(cons.GET_INSTANCES_IDS)
    with open('instances.json', 'r+') as instancesFile:
        dataInstances = json.load(instancesFile)
        # verificar se arquivo ta vazio
        data[cons.INSTANCES_DESCRIPTION] = dataInstances
        endTime = datetime.utcnow().isoformat()
        startTime = (datetime.utcnow() - timedelta(hours=1)).isoformat()

        data[cons.END_TIME_KEY] = endTime
        data[cons.START_TIME_KEY] = startTime

    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()

    collcWithBoto = CWB(data[cons.METRICS_KEY],  data[cons.INSTANCES_DESCRIPTION],
                        data[cons.START_TIME_KEY],  data[cons.END_TIME_KEY], data[cons.PERIOD_KEY])
    collcWithBoto.getMetrics()
