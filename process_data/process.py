import pandas as pd
import os.path
from datetime import date, datetime, timedelta
from log.setup import setup_log
import constants as cons
import json

# TO-DO: remover método

# def createNewDf(datapoints, metric, value):

#     statistics = metric[cons.STATISTICS_KEY]
#     timestampArray = list(map(lambda dtp: (dtp['Timestamp']).timestamp(), datapoints))
#     newDict = {'timestamp': timestampArray}
#     totalRows = len(newDict['timestamp'])
#     for stat in statistics: 
#         statValues = list(map(lambda dtp: dtp[stat], datapoints))
#         newDict[stat] = statValues

#     dimension = metric[cons.DIMENSION_KEY]
#     if(metric[cons.DIMENSION_KEY] == "LoadBalancer"):
#         dimension =  "LoadBalancerName"

#     newDict[dimension] = [value[dimension]] * totalRows
#     newDict[cons.METRIC_NAME_KEY]  = [metric[cons.METRIC_NAME_KEY]]* totalRows


#     if(metric[cons.DIMENSION_KEY] == cons.INSTANCE_ID_KEY):
#         flavor = value['InstanceType']
#         newDict['InstanceType'] = [flavor] * totalRows
   
#     return newDict


def joinMetrics(response, metric, value, info = ''):
    datapoints = response[cons.DATAPOINTS_KEY]
    dts = []
    
    for data in datapoints:
        dt = []
        dt.append(data['Timestamp'].timestamp())
        dt.append(value)
        dt.append(metric['metricName'])
        if(len(info) != 0):
            dt.append(info)
        if 'statistics' in metric:
            for s in metric['statistics']:
                dt.append(data[s])
        dts.append(dt)

    return dts

def editOrCreateFiles(newDict, folderName):
    logger = setup_log()
    newDf = pd.DataFrame(data=newDict)

    today_file = datetime.now().strftime("%m-%d-%Y-%H:%M:%S")

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


def processASGFiles(response):
    autoscalingGroups = response['AutoScalingGroups']
    newDict = {}
    instanceIds, asgNames, timestamp = [], [], []
    asgAplicationName, asgEnvironment, asgName, asgOwner, asgProduct = [], [], [], [], []
    
    currentHour = datetime.now().timestamp()

    for asg in autoscalingGroups:
        qtyInstances = len(list(map(_getInstanceId, asg['Instances'])))
        instanceIds += list(map(_getInstanceId, asg['Instances']))
        asgNames += [asg['AutoScalingGroupName']] * qtyInstances

        tagsFind = [False,False,False,False,False]
        for tag in asg['Tags']:    
            if 'Key' in tag and 'Value' in tag:
                if tag['Key'] == 'AplicationName':
                    tagsFind[0] = True
                    asgAplicationName += [tag['Value']] * qtyInstances
                elif tag['Key'] == 'Environment':
                    tagsFind[1] = True
                    asgEnvironment += [tag['Value']] * qtyInstances
                elif tag['Key'] == 'Name':
                    tagsFind[2] = True
                    asgName += [tag['Value']] * qtyInstances
                elif tag['Key'] == 'Owner':
                    tagsFind[3] = True
                    asgOwner += [tag['Value']] * qtyInstances
                elif tag['Key'] == 'Product':
                    tagsFind[4] = True
                    asgProduct += [tag['Value']] * qtyInstances

        if not tagsFind[0]:
            asgAplicationName += [""] * qtyInstances
        if not tagsFind[1]:
            asgEnvironment += [""] * qtyInstances
        if not tagsFind[2]:
            asgName += [""] * qtyInstances
        if not tagsFind[3]:
            asgOwner += [""] * qtyInstances
        if not tagsFind[4]:
            asgProduct += [""] * qtyInstances

    timestamp = [currentHour] * len(instanceIds)
    newDict = {
        'timestamp': timestamp,
        'InstanceId': instanceIds,
        'AutoscalingGroup': asgNames,
        'AplicationName': asgAplicationName, 
        'Environment': asgEnvironment, 
        'Name': asgName, 
        'Owner': asgOwner,
        'Product': asgProduct
    }

    newDf = pd.DataFrame(data=newDict)

    editOrCreateFiles(newDf, 'asg')


def _getInstanceId(item):
    return item['InstanceId']


def saveRawFile(response):
    today_file = "events-" + date.today().strftime("%Y-%m-%d")
    path = os.path.join(os.getcwd(), "data")
    filePath = path + "/" + today_file + ".csv"

    ActivityId, AutoScalingGroupName, Description, Cause, StartTime,EndTime, StatusCode = [],[],[],[],[],[],[]

    for activity in response['Activities']:
        ActivityId.append(activity['ActivityId'])
        AutoScalingGroupName.append(activity['AutoScalingGroupName'])
        Description.append(activity['Description'])
        Cause.append(activity['Cause'])
        StartTime.append(activity['StartTime'].timestamp())
        EndTime.append(activity['EndTime'].timestamp())
        StatusCode.append(activity['StatusCode'])

    newDict = {
        "ActivityId": ActivityId,
        "AutoScalingGroupName": AutoScalingGroupName,
        "Description": Description,
        "Cause": Cause,
        "StartTime": StartTime,
        "EndTime": EndTime,
        "StatusCode": StatusCode
    }
    newDf = pd.DataFrame(data=newDict)

    editOrCreateFiles(newDf, 'asg-events')
