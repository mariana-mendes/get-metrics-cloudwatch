
#!/usr/bin/env python3

import json
import constants as cons
from datetime import datetime, timedelta, date
from collector.collector_boto import CollectorAgent as CWA
from aws.API import API as api
from deleter.delete_folder import deleteFolderS3 as deleter
from log.setup import setup_log
import os

''' Runs the collector. 
    Adjust the collector range and instantiate the Collector and the Sender'''
with open(cons.CONFIG_FILE, 'r+') as f:
    data = json.load(f)

cwapi = api(data[cons.AWS_CONFIG]["region"])
deleter = deleter(data[cons.AWS_CONFIG])
logger = setup_log()
deleter.delete_folder('out01/')
