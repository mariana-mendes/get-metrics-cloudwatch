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
        statiscs = input('Statistics (separeted by comma): ')
        newDescription = {cons.METRIC_NAME_KEY: metricName,
                          cons.NAMESPACE_KEY: namespace,
                          cons.DIMENSION_KEY: dimension,
                          cons.STATISTICS_KEY: statiscs.split(',')}
        descriptions.append(newDescription)
        print(descriptions)
        ans = input(cons.ASK_FOR_NEW_METRIC)
    return descriptions


def storageNames(descriptions):

    dimensions = set(map(lambda ds: ds[cons.DIMENSION_KEY], descriptions))
    storageNames = {}

    for dim in dimensions:
        storageNames[dim]  = input(cons.ASK_FOLDER_NAMES.format(dim))
       
    return storageNames




def awsconfig():
    region = input("AWS region: ")
    bucket = input("\nBucket: ")
    return {"region": region, "bucket": bucket}


with open(cons.CONFIG_FILE, 'r+') as f:
    data = json.load(f)

    metricsDescription = getMetricDescription()
    data[cons.STORAGE] = storageNames(metricsDescription)
    data[cons.METRICS_KEY] = metricsDescription
    data[cons.AWS_CONFIG] = awsconfig()
    gran = input(cons.GRANURALITY)
    data[cons.PERIOD_KEY] = gran

    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()

    commandString ='cd {} && ./run.py'.format(os.getcwd())

    username = getpass.getuser()
    cron = CronTab(user=username)
    jobCollect = cron.new(command=commandString)
    jobCollect.every(cons.FREQUENCY_COLLECTOR).hours()
    cron.write()
