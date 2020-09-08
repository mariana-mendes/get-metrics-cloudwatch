import pandas as pd
import os.path
from datetime import date
from log.setup import setup_log


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

    path = os.getcwd() + "/data/ec2/" + today_file + ".csv"
    if(os.path.exists(path)):
        dtf = pd.read_csv(today_file + '.csv', index_col=0)
        newOne = dtf.append(newDf, ignore_index=True)
        newOne.to_csv(path)
    else:
        newDf.to_csv(path)


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
    path = os.getcwd() + "/data/asg/" + today_file + ".csv"
    try:
        if(os.path.exists(path)):
            dtf = pd.read_csv(path, index_col=0)
            newOne = dtf.append(newDf, ignore_index=True)
            newOne.to_csv(path)
        else:
            newDf.to_csv(path)
    except Exception as e:
        logger.error("erro ao criar arquivos", e.__class__)
