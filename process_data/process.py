import pandas as pd
import os.path
from datetime import date, datetime, timedelta
from log.setup import setup_log
import constants as cons


def createNewDf(datapoints, metric, metricDimension, value):
    dimension = metric[cons.DIMENSION_KEY]
    time, maximum, minimum, average = [], [], [], []

    for dtp in datapoints:
        dt = (dtp['Timestamp']).timestamp()
        time.append(dt)
        maximum.append(dtp['Maximum'])
        minimum.append(dtp['Minimum'])
        average.append(dtp['Average'])

    totalRows = len(time)
    idColumn = [value] * totalRows
    metricColumn = [metric[cons.METRIC_NAME_KEY]] * totalRows
    infoColumn = [''] * totalRows

    if (not isinstance(value, str)):
        idColumn = [value["InstanceId"]] * totalRows
        infoColumn = [value["InstanceType"]] * totalRows

    newDict = {
        'timestamp': time,
        dimension: idColumn,
        'metric': metricColumn,
        'max': maximum,
        'min': minimum,
        'avg': average,
        'info': infoColumn
    }

    return newDict


def _isDataFromToday(dtp):
    return (dtp['Timestamp']).replace(tzinfo=None).day == date.today().day


def _isDataFromYesterday(dtp):
    return (dtp['Timestamp']).replace(tzinfo=None).day != date.today().day


def joinMetrics(response, metric, metricDimension, value, folderName):
    datapoints = response[cons.DATAPOINTS_KEY]

    yesterdayDTP = list(filter(_isDataFromYesterday, datapoints))

    if (len(yesterdayDTP) != 0):
        yesterdayDf = createNewDf(yesterdayDTP, metric, metricDimension, value)
        editOrCreateFiles(yesterdayDf, folderName)

    todayDTP = list(filter(_isDataFromToday, datapoints))

    if (len(todayDTP) != 0):
        todayDf = createNewDf(todayDTP, metric, metricDimension, value)
        editOrCreateFiles(todayDf, folderName)


def editOrCreateFiles(newDict, folderName):
    logger = setup_log()
    newDf = pd.DataFrame(data=newDict)

    today_file = date.today().strftime("%Y-%m-%d")

    path = os.path.join(os.getcwd(), "data", folderName)
    filePath = path + "/" + today_file + ".csv"

    if (not os.path.exists(path)):
        os.mkdir(path)

    if (not newDf.empty):
        try:
            if (os.path.exists(filePath)):
                dtf = pd.read_csv(filePath, index_col=0)
                newOne = dtf.append(newDf, ignore_index=True)
                newOne.to_csv(filePath)
            else:
                newDf.to_csv(filePath)
        except Exception as e:
            logger.error("Erro ao criar arquivos", e.__class__)



