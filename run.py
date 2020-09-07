#!/usr/bin/env python3

import os
import sys
import json
import constants as cons
from datetime import datetime, timedelta
from collector.collector_boto import CollectorAgentWithBoto as CWB
from sender.send_files import Sender as sender
from log.setup import setup_log

with open(cons.CONFIG_FILE, 'r+') as f:
    data = json.load(f)

    # os.system(cons.GET_INSTANCES_IDS)

    with open(cons.INSTANCES_FILE, 'r+') as instancesFile:
        dataInstances = json.load(instancesFile)
        data[cons.INSTANCES_DESCRIPTION] = dataInstances

        endTime = datetime.utcnow().isoformat()
        startTime = (datetime.utcnow() -
                     timedelta(hours=cons.FREQUENCY_COLLECTOR)).isoformat()
        data[cons.END_TIME_KEY] = endTime
        data[cons.START_TIME_KEY] = startTime

    # os.system(cons.GET_AUTOSCALING_GROUPS)
    with open(cons.GROUPS_FILE, 'r+') as groupsFile:
        names = []
        dataGroups = json.load(groupsFile)["AutoScalingGroups"]
        for group in dataGroups:
            names.append(group["AutoScalingGroupName"])
        data[cons.GROUPS_DESCRIPTION] = names

    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()


collcWithBoto = CWB(data[cons.METRICS_KEY],  data[cons.INSTANCES_DESCRIPTION], data[cons.GROUPS_DESCRIPTION],
                    data[cons.START_TIME_KEY],  data[cons.END_TIME_KEY], data[cons.PERIOD_KEY])

# pegar nomes dos arquivos
today_file_ec2 = "ec2-" + date.today().strftime("%Y-%m-%d")
today_file_asg = "asg-" + date.today().strftime("%Y-%m-%d")

senderEC2 = sender(today_file_ec2)
senderASG = sender(today_file_asg)

logger = setup_log()
logger.info(cons.STARTING_COLLECTOR)
collcWithBoto.getMetrics()
senderEC2.send_files()
senderASG.send_files()
