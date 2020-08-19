# get-metrics-cloudwatch

### TO-DO: arranjar um nome legal.

### Setup instance
 
* Launch an EC2 instance. 
* Create an IAM Role 
    * Create a policy: 
      Using json editor, your policy should look like this
      ```
         {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "VisualEditor0",
                "Effect": "Allow",
                "Action": [
                    "cloudwatch:PutMetricData",
                    "ec2:DescribeTags",
                    "cloudwatch:GetMetricStatistics",
                    "cloudwatch:ListMetrics"
                ],
                "Resource": "*"
            }
        ]
       }
      ```
* Install python 
* Install aws cli 
* Run: `aws config` 
  
### Setup collector

`git clone https://github.com/mariana-mendes/get-metrics-cloudwatch.git && cd get-metrics-cloudwatch` 

run: `crontab -e`, in the end of file add:`* * * cd <YOUR-PATH>/get-metrics-cloudwatch && python3 run.py`
 

![Diagrama](https://github.com/mariana-mendes/get-metrics-cloudwatch/blob/master/diagrama.png)
