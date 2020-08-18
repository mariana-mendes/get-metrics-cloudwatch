#!/usr/bin/python

import os 
import sys
import json 
import constants as cons
import time
sys.path.append("./collector")

from collector import CollectorAgent as CW

with open('config.json', 'r+') as f:

  # os.system(cons.GET_INSTANCES_IDS)

  with open('instances.json', 'r+') as i:
    data = json.load(f)

    ## get all ec2 instances
    idInstances = []
    instances = json.load(i)
    for a in instances:
      print a[0]['id']
      idInstances.append(a[0]['id'])


  ## add all ids into config file
  data[cons.IDS_KEY] = idInstances

  print(cons.HELLO)
  print json.dumps(data, indent=2, sort_keys=True)
 

  ## Config in case of the user want just one consult a especific period

  # ans = raw_input(cons.ASK_FOR_CONFIG)

  # if(ans == "Y"): 
  #   instances = map(str,raw_input("Enter field " + cons.IDS_KEY + ": ").split())
    
  #   config_fields = [cons.METRIC_KEY, cons.START_TIME_KEY, cons.END_TIME_KEY, cons.PERIOD_KEY]

  #   for field in config_fields:
  #     value = raw_input("Enter field " + field + ": ")
  #     data[field] = value


  f.seek(0)        
  json.dump(data, f, indent=4)
  f.truncate()    
  print cons.RESULT_FILE
  print json.dumps(data, indent=2, sort_keys=True)


  collc = CW(data[cons.METRIC_KEY],  data[cons.IDS_KEY],  data[cons.START_TIME_KEY],  data[cons.END_TIME_KEY], data[cons.PERIOD_KEY])
  collc.getMetrics()








