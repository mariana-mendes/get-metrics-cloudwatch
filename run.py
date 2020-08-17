import os 
import sys
import json 
import constants as cons
sys.path.append("./collector")

from collector import CollectorAgent as CW

with open('config.json', 'r+') as f:

  data = json.load(f)
  print(cons.HELLO)
  print json.dumps(data, indent=2, sort_keys=True)

  ans = raw_input(cons.ASK_FOR_CONFIG)

  if(ans == "Y"): 
    instances = map(str,raw_input("Enter field " + cons.IDS_KEY + ": ").split())
    data[cons.IDS_KEY] = instances
    
    config_fields = [cons.METRIC_KEY, cons.START_TIME_KEY, cons.END_TIME_KEY, cons.PERIOD_KEY]

    for field in config_fields:
      value = raw_input("Enter field " + field + ": ")
      data[field] = value


    f.seek(0)        
    json.dump(data, f, indent=4)
    f.truncate()    
    print cons.RESULT_FILE
    print json.dumps(data, indent=2, sort_keys=True)


  collc = CW(data[cons.METRIC_KEY],  data[cons.IDS_KEY],  data[cons.START_TIME_KEY],  data[cons.END_TIME_KEY], data[cons.PERIOD_KEY])
  collc.getMetrics()






