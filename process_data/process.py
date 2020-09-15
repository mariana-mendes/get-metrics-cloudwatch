import pandas as pd
import os.path
from datetime import date, datetime, timedelta
from log.setup import setup_log
import constants as cons

def joinMetrics(response, metric, metricDimension, value, folderName):
    logger = setup_log()
    datapoints = response[cons.DATAPOINTS_KEY]
    dimension = metric[cons.DIMENSION_KEY]

    time,maximum,minimum,average = [], [], [], []
    
    newDictYstd = {'timestamp': [], dimension: [], 'metric': [], 'max': [], 'min': [], 'avg': []}
    hasData = False
    for dtp in datapoints:
        ## tratar problema da coleta às 00:00
        dt = (dtp['Timestamp']).replace(tzinfo=None)
        if(dt.day != date.today().day):
            hasData = True
            newDictYstd["timestamp"].append(dt.strftime("%m/%d/%Y, %H:%M:%S"))
            newDictYstd["min"].append(dtp['Minimum'])
            newDictYstd["max"].append(dtp['Maximum'])
            newDictYstd["avg"].append(dtp['Average'])
        else:
            time.append(dt.strftime("%m/%d/%Y, %H:%M:%S"))
            maximum.append(dtp['Maximum'])
            minimum.append(dtp['Minimum'])
            average.append(dtp['Average'])

    totalRows = len(time)
    idColumn = [value] * totalRows
    metricColumn = [metric[cons.METRIC_NAME_KEY]] * totalRows
    
    newDict = {
        'timestamp': time,
        dimension: idColumn,
        'metric': metricColumn,
        'max': maximum,
        'min': minimum,
        'avg': average
    }

    ## tratar problema da coleta às 00:00
    newDictYstd[dimension] =  [value] * len(newDictYstd['timestamp'])
    newDictYstd['metric'] = [metric[cons.METRIC_NAME_KEY]] * len(newDictYstd['timestamp'])

    newDf = pd.DataFrame(data=newDict)
    today_file = date.today().strftime("%Y-%m-%d")

    path =  os.path.join(os.getcwd(),"data", folderName)
    filePath = path + "/" + today_file + ".csv"

    if(not os.path.exists(path)):
         os.mkdir(path)

    if(not newDf.empty):
        try:
            if(os.path.exists(filePath)):
                dtf = pd.read_csv(filePath, index_col=0)
                newOne = dtf.append(newDf, ignore_index=True)
                newOne.to_csv(filePath)
            else:
                newDf.to_csv(filePath)
        except Exception as e:
            logger.error("Erro ao criar arquivos", e.__class__)
    
    ## tratar problema da coleta às 00:00
    yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")
    filePath2 = path + "/" + yesterday + ".csv"
    if(hasData & os.path.exists(filePath2)):
        dtf = pd.read_csv(filePath2, index_col=0)
        newDf2 = pd.DataFrame(data=newDictYstd)
        newOne = dtf.append(newDf2, ignore_index=True)
        newOne.to_csv(filePath2)
