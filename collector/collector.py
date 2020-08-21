import os
from string import Template
import constants as cons


class CollectorAgent:
  def __init__(self, metricName, instanceDescription, start, end, period):
    self.metricName = metricName
    self.instanceDescription = instanceDescription
    self.start = start
    self.end = end
    self.period = period



  def getMetrics(self):
    for instance in self.instanceDescription:
      # try:
        print(instance)
        command = Template(cons.GET_CPU_UTILIZATION)
        # commandString = command.substitute(metric=self.metricName[0], idInstance=instanceId, period=self.period, start=self.start, end=self.end, id=id)
        # print('>' + commandString)
        # os.system(commandString)
      # except Exception as e:
        # print("Oops!", e.__class__, "occurred.")
        # print()
   

  def getAWSMetric():
    return 0

  def getCWAMetric(): 
    return 0
