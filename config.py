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
        dimension = input('\nDimension:')
        newDescription = {cons.METRIC_NAME_KEY: metricName,
                          cons.NAMESPACE_KEY: namespace,
                          cons.DIMENSION_KEY: dimension}
        descriptions.append(newDescription)
        print(descriptions)
        ans = input(cons.ASK_FOR_NEW_METRIC)
    return descriptions


def storageNames(descriptions):

    dimensions = []
    for ds in descriptions:
        dimensions.append(ds[cons.DIMENSION_KEY])

    storageNames = {}
    for dim in dimensions:
        storageFolder = input("For metrics retrieve with dimension: " + dim)
        storageNames[dim] = storageFolder

    return storageNames


with open(cons.CONFIG_FILE, 'r+') as f:
    data = json.load(f)

    metricsDescription = getMetricDescription()
    data[cons.STORAGE] = storageNames(metricsDescription)
    data[cons.METRICS_KEY] = metricsDescription
    gran = input(cons.GRANURALITY)
    data[cons.PERIOD_KEY] = gran

    print(cons.INFO_INSTANCES)
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()

    path = os.getcwd()

    commandString = 'cd ' + path + ' && ' + './run.py'

    username = getpass.getuser()
    cron = CronTab(user=username)
    jobCollect = cron.new(command=commandString)
    jobCollect.every(cons.FREQUENCY_COLLECTOR).hours()
    cron.write()
