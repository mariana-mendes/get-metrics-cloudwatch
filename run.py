#!/usr/bin/env python3

import os
import sys
import json
import constants as cons
from datetime import datetime, timedelta, date
from collector.collector_boto import CollectorAgent as CWA
from sender.send_files import Sender as sender
from log.setup import setup_log

with open(cons.CONFIG_FILE, 'r+') as f:
    data = json.load(f)

    os.system(cons.GET_INSTANCES_IDS)

    with open(cons.INSTANCES_FILE, 'r+') as instancesFile:
        dataInstances = json.load(instancesFile)
        instanceIdValues = []

        for instance in dataInstances:
            instanceIdValues.append(instance[0])

        data[cons.DIMENSIONS_VALUES][cons.INSTANCE_ID_KEY] = instanceIdValues

        endTime = datetime.utcnow().isoformat()
        startTime = (datetime.utcnow() -
                     timedelta(hours=cons.FREQUENCY_COLLECTOR)).isoformat()
        data[cons.END_TIME_KEY] = endTime
        data[cons.START_TIME_KEY] = startTime

    os.system(cons.GET_AUTOSCALING_GROUPS)

    with open(cons.GROUPS_FILE, 'r+') as groupsFile:
        names = []
        dataGroups = json.load(groupsFile)["AutoScalingGroups"]

        for group in dataGroups:
            names.append(
                {cons.AUTOSCALINGGROUP_ID_KEY: group[cons.AUTOSCALINGGROUP_ID_KEY]})
        data[cons.DIMENSIONS_VALUES][cons.AUTOSCALINGGROUP_ID_KEY] = names

    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()

    collector = CWA(data[cons.METRICS_KEY],  data[cons.DIMENSIONS_VALUES],
                    data[cons.START_TIME_KEY],  data[cons.END_TIME_KEY], data[cons.PERIOD_KEY], data[cons.STORAGE])


sender = sender()
logger = setup_log()
logger.info(cons.STARTING_COLLECTOR)
collector.getMetrics()
sender.send_files()
