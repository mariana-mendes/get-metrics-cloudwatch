#!/usr/bin/env python3

import os
import sys
import json
import constants as cons
from crontab import CronTab
import getpass


def getMetricDescription():
    ans = input(cons.ASK_FOR_NEW_METRIC)
    descriptions = []

    while ans == '1':
        metricName = input("Metric name:  ")
        namespace = input('\nNamespace: ')
        newDescription = {cons.METRIC_NAME_KEY: metricName,
                          cons.NAMESPACE_KEY: namespace}
        descriptions.append(newDescription)
        print(descriptions)
        ans = input(cons.ASK_FOR_NEW_METRIC)
    return descriptions


with open(cons.CONFIG_FILE, 'r+') as f:
    data = json.load(f)

    metricsDescription = getMetricDescription()
    data[cons.METRICS_KEY] = metricsDescription
    gran = input(cons.GRANURALITY)
    data[cons.PERIOD_KEY] = gran

    print(cons.INFO_INSTANCES)
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()

    path = os.getcwd()

    commandString = 'cd ' + path + ' && ' + './run.py'
    commandFiles = 'cd ' + path + ' && ' + './send_files.py'

    username = getpass.getuser()
    cron = CronTab(user=username)
    jobCollect = cron.new(command=commandString)
    jobSendFiles = cron.new(command=commandFiles)
    jobCollect.hour.every(cons.FREQUENCY_COLLECTOR)
    jobSendFiles.hour.every(cons.FREQUENCY_S3)
    cron.write()
