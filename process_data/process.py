import pandas as pd
import os.path
from datetime import date, datetime, timedelta
from log.setup import setup_log
import constants as cons


def createNewDf(datapoints, metric, value):
    statistics = metric[cons.STATISTICS_KEY]
    timestampArray = list(map(lambda dtp: (dtp['Timestamp']).timestamp(), datapoints))
    newDict = {'timestamp': timestampArray}
    totalRows = len(newDict['timestamp'])
    for stat in statistics: 
        statValues = list(map(lambda dtp: dtp[stat], datapoints))
        newDict[stat] = statValues

    dimension = metric[cons.DIMENSION_KEY]
    newDict[dimension] = [value[dimension]] * totalRows
    newDict[cons.METRIC_NAME_KEY]  = [metric[cons.METRIC_NAME_KEY]]* totalRows


    if(metric[cons.DIMENSION_KEY] == cons.INSTANCE_ID_KEY):
        flavor = value['InstanceType']
        newDict['InstanceType'] = [flavor] * totalRows
   
    return newDict


def joinMetrics(response, metric, value, folderName):
    datapoints = response[cons.DATAPOINTS_KEY]

    yesterdayDTP = list(  filter(  (lambda dtp: dtp['Timestamp'].replace(tzinfo=None).day != date.today().day) , datapoints  ))

    if (len(yesterdayDTP) != 0):
        yesterdayDf = createNewDf(yesterdayDTP, metric, value)
        editOrCreateFiles(yesterdayDf, folderName)

    todayDTP = list(  filter(  (lambda dtp: dtp['Timestamp'].replace(tzinfo=None).day == date.today().day) , datapoints  ))

    if (len(todayDTP) != 0):
        todayDf = createNewDf(todayDTP, metric, value)
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



