#!/usr/bin/env python3

from collector.collector_boto import CollectorAgent as CWA
from sender import send_files
from datetime import datetime, timedelta, date
import constants as cons
import json

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

collector = CWA(data[cons.METRICS_KEY],  data[cons.START_TIME_KEY],  data[cons.END_TIME_KEY], data[cons.PERIOD_KEY], data[cons.STORAGE], data[cons.AWS_CONFIG])
collector.createDescriptionsASGFile()
collector.createEventsASGFile()
