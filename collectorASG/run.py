#!/usr/bin/env python3

from collector_asg import CollectorAgentASG as CWASG
from sender import send_files
import json

collectorASG = CWASG()
collectorASG.describeASG()
collectorASG.getHistoricEvents()

with open("../config.json", 'r+') as f:
    data = json.load(f)
    send_files(data["aws-config"])
