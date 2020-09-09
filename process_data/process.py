import pandas as pd
import os.path
from datetime import date
from log.setup import setup_log
import constants as cons


def joinMetrics(response, idValue, metricName, folderName):
    logger = setup_log()
    datapoints = response[cons.DATAPOINTS_KEY]
    totalRows = len(datapoints)
    metricColumn = [metricName] * totalRows
    idColumn = [idValue] * totalRows
    print(idValue)

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
        idValue: idColumn,
        'metric': metricColumn,
        'max': maximum,
        'min': minimum,
        'avg': average
    }
    newDf = pd.DataFrame(data=newDict)
    today_file = date.today().strftime("%Y-%m-%d")

    path = os.getcwd() + "/data/" + folderName + "/" + today_file + ".csv"
    try:
        if(os.path.exists(path)):
            dtf = pd.read_csv(path, index_col=0)
            newOne = dtf.append(newDf, ignore_index=True)
            newOne.to_csv(path)
        else:
            newDf.to_csv(path)
    except Exception as e:
        logger.error("Erro ao criar arquivos", e.__class__)
