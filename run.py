#!/usr/bin/env python3

import json
import constants as cons
from datetime import datetime, timedelta, date
from collector.collector_boto import CollectorAgent as CWA
from aws.API import API as api
from sender.send_files import Sender as sender
from log.setup import setup_log

with open(cons.CONFIG_FILE, 'r+') as f:
    data = json.load(f)
    endTime = datetime.utcnow().isoformat()
    startTime = (datetime.utcnow() -
                  timedelta(hours=cons.FREQUENCY_COLLECTOR)).isoformat()
    data[cons.END_TIME_KEY] = endTime
    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()

collector = CWA(data[cons.METRICS_KEY],  data[cons.START_TIME_KEY],  data[cons.END_TIME_KEY], data[cons.PERIOD_KEY], data[cons.STORAGE])

cwapi = api()
sender = sender()
logger = setup_log()
logger.info(cons.STARTING_COLLECTOR)
collector.getMetrics()
sender.send_files()
