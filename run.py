#!/usr/bin/env python3

import os 
import sys
import json 
import constants as cons
import time

from collector.collector import CollectorAgent as CW
  
with open('config.json', 'r+') as f:

  with open('instances.json', 'r+') as i:
    data = json.load(f)

    ## get all ec2 instances
    idInstances = []
    instances = json.load(i)
    for a in instances:
      print(a[0]['id'])
      idInstances.append(a[0]['id'])

  f.seek(0)        
  json.dump(data, f, indent=4)
  f.truncate()    
  print(cons.RESULT_FILE)
  # print(json.dumps(data, indent=2, sort_keys=True))


  collc = CW(data[cons.METRIC_KEY],  data[cons.INSTANCES_DESCRIPTION],  data[cons.START_TIME_KEY],  data[cons.END_TIME_KEY], data[cons.PERIOD_KEY])
  collc.getMetrics()








