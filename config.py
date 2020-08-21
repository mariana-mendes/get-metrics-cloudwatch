#!/usr/bin/env python3

import os 
import sys
import json 
import constants as cons
from crontab import CronTab
import getpass
from collector.collector import CollectorAgent as CW
  

def getMetricDescription():
  ans = input(cons.ASK_FOR_NEW_METRIC)
  descriptions = []

  while ans == '1':
    metricName = input("Metric name:  ")
    namespace = input(' \n Namespace: ')
    newDescription ={'metricName': metricName, 'namespace':namespace}
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

    print(cons.RESULT_FILE)
    print(json.dumps(data, indent=2, sort_keys=True))
 
    print('Getting Instances Description...\n')
    instancesDescription =  os.system(cons.GET_INSTANCES_IDS)
    data[cons.INSTANCES_DESCRIPTION] = instancesDescription

    f.seek(0)        
    json.dump(data, f, indent=4)
    f.truncate()   

    path = os.getcwd()

    commandString = '@hourly cd ' + path + ' && ' + './run.py'

    print('Almost done! Editing your crontab file... ')
    username = getpass.getuser()
    cron = CronTab(user=username)
    job = cron.new(command=commandString)
    cron.write()


  else:
    print('to-do')
    ## te vira e roda o comando xD
