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
        namespace = input('\n Namespace: ')
        newDescription = {'metricName': metricName, 'namespace': namespace}
        descriptions.append(newDescription)
        print(descriptions)
        ans = input(cons.ASK_FOR_NEW_METRIC)
    return descriptions


with open('config.json', 'r+') as f:
    data = json.load(f)
    ans = input(cons.ASK_FOR_COLLECT_TYPE)

    if(ans == '1'):
        metricsDescription = getMetricDescription()
        data[cons.METRICS_KEY] = metricsDescription

        gran = input("Granularity of datapoints: ")
        data[cons.PERIOD_KEY] = gran

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

        path = os.getcwd()

        commandString = 'cd ' + path + ' && ' + './run.py'

        username = getpass.getuser()
        cron = CronTab(user=username)
        job = cron.new(command=commandString)
        job.minute.every(3)
        cron.write()

        commandFiles = 'cd ' + path + ' && ' + './send_files.py'
        cron = CronTab(user=username)
        job = cron.new(command=commandFiles)
        job.minute.every(5)
        cron.write()

    else:
        print('to-do')
        # te vira e roda o comando xD
