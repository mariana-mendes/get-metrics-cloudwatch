#!/usr/bin/env python3

import os 
import sys
import json 
import constants as cons
import time
from datetime import datetime, timedelta

from collector.collector import CollectorAgent as CW

  
with open('config.json', 'r+') as f:
  data = json.load(f)
  os.system(cons.GET_INSTANCES_IDS)
  with open('instances.json', 'r+') as instancesFile:
    dataInstances = json.load(instancesFile)
    ## verificar se arquivo ta vazio 
    data[cons.INSTANCES_DESCRIPTION] = dataInstances
    startTime = datetime.utcnow().isoformat()
    endTime = (datetime.utcnow() - timedelta(hours=1)).isoformat()

  f.seek(0)        
  json.dump(data, f, indent=4)
  f.truncate()    

  collc = CW(data[cons.METRICS_KEY],  data[cons.INSTANCES_DESCRIPTION],  data[cons.START_TIME_KEY],  data[cons.END_TIME_KEY], data[cons.PERIOD_KEY])
  collc.getMetrics()
