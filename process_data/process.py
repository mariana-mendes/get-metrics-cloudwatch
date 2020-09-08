import pandas as pd
import os.path
from datetime import date


def joinMetricsEC2(response, idInstance, metricName):
    datapoints = response["Datapoints"]
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

    newDict = {
        'timestamp': time,
        'instanceID': idColumn,
        'metric': metricColumn,
        'max': maximum,
        'min': minimum,
        'avg': average
    }
    newDf = pd.DataFrame(data=newDict)
    today_file = date.today().strftime("%Y-%m-%d")

    if(os.path.exists(today_file + '.csv')):
        dtf = pd.read_csv(today_file + '.csv', index_col=0)
        newOne = dtf.append(newDf, ignore_index=True)
        newOne.to_csv('/data/ec2', today_file + ".csv")
    else:
        newDf.to_csv('/data/ec2', today_file + ".csv")


def joinMetricsASG(response, groupName, metricName):
    logger = setup_log()
    datapoints = response["Datapoints"]
    totalRows = len(datapoints)
    metricColumn = [metricName] * totalRows
    idColumn = [groupName] * totalRows

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

    newDict = {
        'timestamp': time,
        'groupName': idColumn,
        'metric': metricColumn,
        'max': maximum,
        'min': minimum,
        'avg': average
    }
    newDf = pd.DataFrame(data=newDict)
    today_file = date.today().strftime("%Y-%m-%d")

    try:
    if(os.path.exists(today_file + '.csv')):
        dtf = pd.read_csv(today_file + '.csv', index_col=0)
        newOne = dtf.append(newDf, ignore_index=True)
        newOne.to_csv('/data/asg', today_file + ".csv")
    else:
        newDf.to_csv('/data/asg', today_file + ".csv")
    except Exception e:
        logger.error("erro ao criar arquivos", e.__class__)
