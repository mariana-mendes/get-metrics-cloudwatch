#!/usr/bin/env python3

import json
import constants as cons
from datetime import datetime, timedelta, date
from collector.collector_boto import CollectorAgent as CWA
from aws.API import API as api
from sender.sendS3 import SendS3 as sender
from log.setup import setup_log
import os

''' Runs the collector. 
    Adjust the collector range and instantiate the Collector and the Sender'''
with open(cons.CONFIG_FILE, 'r+') as f:
    data = json.load(f)
    endTime = datetime.utcnow().isoformat()
    startTime = (datetime.utcnow() -
                  timedelta(hours=cons.FREQUENCY_COLLECTOR)).isoformat()
    data[cons.END_TIME_KEY] = endTime
    data[cons.START_TIME_KEY] = startTime
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()

cwapi = api(data[cons.AWS_CONFIG]["region"])
sender = sender(data[cons.AWS_CONFIG])
logger = setup_log()
sender.send_folder('/home/gabriela/mari/out01/')
