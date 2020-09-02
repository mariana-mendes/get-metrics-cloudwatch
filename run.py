#!/usr/bin/env python3

import os
import sys
import json
import constants as cons
from datetime import datetime, timedelta
from collector.collector_boto import CollectorAgentWithBoto as CWB
from log.setup import setup_log
from send_files import send_file

with open(cons.CONFIG_FILE, 'r+') as f:
    data = json.load(f)

    os.system(cons.GET_INSTANCES_IDS)

    with open(cons.INSTANCES_FILE, 'r+') as instancesFile:
        dataInstances = json.load(instancesFile)
        data[cons.INSTANCES_DESCRIPTION] = dataInstances

        endTime = datetime.utcnow().isoformat()
        startTime = (datetime.utcnow() -
                     timedelta(hours=cons.FREQUENCY_COLLECTOR)).isoformat()
        data[cons.END_TIME_KEY] = endTime
        data[cons.START_TIME_KEY] = startTime

    f.seek(0)
    json.dump(data, f, indent=4)
    f.truncate()

collcWithBoto = CWB(data[cons.METRICS_KEY],  data[cons.INSTANCES_DESCRIPTION],
                    data[cons.START_TIME_KEY],  data[cons.END_TIME_KEY], data[cons.PERIOD_KEY])

logger = setup_log()
logger.info(cons.STARTING_COLLECTOR)
collcWithBoto.getMetrics()
send_file()
