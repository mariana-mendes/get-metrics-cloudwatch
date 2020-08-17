import os 
import sys
import json 
sys.path.append("./collector")

from collector import CollectorAgent as CW

# Opening JSON file 
with open('config.json', 'r+') as f:
  ## detect instances ids
  ## run command to get id list

  data = json.load(f)
  print("Hello! The current config is: \n")
  print data
  ans = raw_input("Do you want edit this file? [Y/n]: ")
  if(ans == "Y"): 
    instances = map(str,raw_input('enter instances ids').split())
    metric = raw_input('metric name')
    start = raw_input('start')
    end = raw_input('end')
    period = raw_input('period')
    data['instanceIds'] = instances
    data['metricName'] = metric
    data['startTime'] = start
    data['endTime'] = end
    data['period'] = period
    f.seek(0)        
    json.dump(data, f, indent=4)
    f.truncate()    
    print "json file result "
    print data
  collc = CW(data['metricName'],  data['instanceIds'],  data['startTime'],  data['endTime'], data['period'])
  collc.getMetrics()






