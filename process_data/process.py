import pandas as pd
from datetime import datetime, timedelta, date
import os.path


def joinMetrics(response, idInstance, metricName):
    datapoints = response["Datapoints"]
    # static fields
    totalRows = len(datapoints)
    metricColumn = [metricName] * totalRows
    idColumn = [idInstance] * totalRows

    time = []
    maximum = []
    minimum = []
    average = []

    for dtp in datapoints:
        dt = (dtp['Timestamp']).replace(tzinfo=None)
        time.append(dt.strftime("%m/%d/%Y, %H:%M:%S"))
        maximum.append(dtp['Maximum'])
        minimum.append(dtp['Minimum'])
        average.append(dtp['Average'])

    newDf = {
        'timestamp': time,
        'instanceID': idColumn,
        'metric': metricColumn,
        'max': maximum,
        'min': minimum,
        'avg': average
    }
    df = pd.DataFrame(data=newDf)

    today_file = date.today().strftime("%Y-%m-%d")

    if(os.path.exists(today_file + '.csv')):
        dtf = pd.read_csv(today_file + '.csv')
        dtf.append(df, ignore_index=True, sort=False)
    else:
        df.to_csv(today_file + ".csv")
