#!/usr/bin/env python3

import os 
import sys
import json 
import constants as cons
import time

from collector.collector import CollectorAgent as CW
  
with open('config.json', 'r+') as f:
  data = json.load(f)

  # os.system(cons.GET_INSTANCES_IDS)

  ## Config in case of the user want just one consult a especific period
  ## First config for json in terminal 

  specificPeriod = raw_input('1. Collect metric in a specific time window \n 2. Automatically collect metrics starting now\n')

  if(specificPeriod == '1'): 
    ans = raw_input(cons.ASK_FOR_CONFIG)

    if(ans == "Y"): 
      ### perguntar se quer pra instancias especificas ou todas
      # instances = map(str,raw_input("Enter field " + cons.IDS_KEY + ": ").split())
      config_fields = [cons.METRIC_KEY, cons.START_TIME_KEY, cons.END_TIME_KEY, cons.PERIOD_KEY]
      for field in config_fields:
        value = raw_input("Enter field " + field + ": ")
        data[field] = value

    f.seek(0)        
    json.dump(data, f, indent=4)
    f.truncate()    
    ### revisar arquivo
    print(cons.RESULT_FILE)
    print(json.dumps(data, indent=2, sort_keys=True))

  else: 
    period = raw_input('Specify the collect period (60s, 300s,...)')
    metrics = map(str,raw_input('Which metrics do you want? (CPUUtilization, mem_usage)').split())

    data['period'] = period
    data['metricName'] = metrics

    f.seek(0)        
    json.dump(data, f, indent=4)
    f.truncate()    
    print(cons.RESULT_FILE)
    print(json.dumps(data, indent=2, sort_keys=True))


    print('Almost done! Now you need to add this: * * * * .......... in your contrab file.')







