import os
from string import Template


class CollectorAgent:
  def __init__(self, metricName, instanceIds, start, end, period):
    self.metricName = metricName
    self.instanceIds = instanceIds
    self.start = start
    self.end = end
    self.period = period

  def getMetrics(self):
    for id in self.instanceIds:
      try:
        command = Template("aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name $metric --dimensions Name=InstanceId,Value=$idInstance --period $period  --statistics 'Average' --start-time $start --end-time $end  --query 'sort_by(Datapoints,&Timestamp)[*]' >> ./data/$id.json")
        commandString = command.substitute(metric=self.metricName, idInstance=id, period=self.period, start=self.start, end=self.end, id=id)
        os.system(commandString)
      except Exception as e:
        print("Oops!", e.__class__, "occurred.")
        print()
   

