HELLO = "Hello! The current config is: \n"
ASK_FOR_CONFIG = "Do you want edit this file? [Y/n]: "
ASK_FOR_COLLECT_TYPE = "Hello!\n1. I want to collect metrics for all instances continous and automatically\n2. I want to specify which instances and a specific period"
RESULT_FILE = "\n This is your config file. Is this correct? [Y/n] "
INSTANCES_DESCRIPTION = "instancesDescription"
START_TIME_KEY = "startTime"
END_TIME_KEY = "endTime"
PERIOD_KEY = "period"
METRICS_KEY = "metricsDescription"
GET_INSTANCES_IDS = "aws ec2 describe-instances --query 'Reservations[*].Instances[*].{id:InstanceId,type:InstanceType,img:ImageId}' --output json > instances.json"
GET_METRIC_AWS = "aws cloudwatch get-metric-statistics --namespace AWS/EC2 --metric-name $metric --dimensions Name=InstanceId,Value=$idInstance --period $period  --statistics 'Average' --start-time $start --end-time $end  --query 'sort_by(Datapoints,&Timestamp)[*]' >> ./data/aws/$id.json"
GET_METRIC_CWAGENT = "aws cloudwatch get-metric-statistics --namespace CWAgent --metric-name $metric --dimensions Name=InstanceId,Value=$idInstance Name=ImageId,Value=$img Name=InstanceType,Value=$type --period $period  --statistics 'Average' --start-time $start --end-time $end --query 'sort_by(Datapoints,&Timestamp)[*]'  >> ./data/cw/$id.json "
ASK_FOR_NEW_METRIC = "\n1. I want to specify a new metric\n2. I already choose my metrics"
