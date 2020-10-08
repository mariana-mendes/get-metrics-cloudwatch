import pandas as pd
import os.path
from datetime import date, datetime, timedelta


def processASGFiles(response):
    autoscalingGroups = response['AutoScalingGroups']

    instanceIds, asgNames, timestamp = [], [], []

    currentHour = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")

    for asg in autoscalingGroups:
        qtyInstances = len(list(map(_getInstanceId, asg['Instances'])))
        instanceIds += list(map(_getInstanceId, asg['Instances']))
        asgNames += [asg['AutoScalingGroupName']] * qtyInstances

    timestamp = [currentHour] * len(instanceIds)
    newDict = {
        'timestamp': timestamp,
        'InstanceId': instanceIds,
        'AutoscalingGroup': asgNames
    }
    newDf = pd.DataFrame(data=newDict)

    today_file = date.today().strftime("%Y-%m-%d")
    path = os.path.join(os.getcwd(), "data")
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
            print("Erro ao criar arquivos", e.__class__)


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
        StartTime.append(activity['StartTime'].replace(
            tzinfo=None).strftime("%m/%d/%Y, %H:%M:%S"))
        EndTime.append(activity['EndTime'].replace(
            tzinfo=None).strftime("%m/%d/%Y, %H:%M:%S"))
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

    if (not newDf.empty):
        try:
            if (os.path.exists(filePath)):
                dtf = pd.read_csv(filePath, index_col=0)
                newOne = dtf.append(newDf, ignore_index=True)
                newOne.to_csv(filePath)
            else:
                newDf.to_csv(filePath)
        except Exception as e:
            print("Erro ao criar arquivos", e.__class__)
