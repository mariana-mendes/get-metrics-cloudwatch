# get-metrics-cloudwatch


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
     
### Inital config 
* Clone the repo:  $ `git clone https://github.com/mariana-mendes/get-metrics-cloudwatch.git && cd get-metrics-cloudwatch` 
* Install dependencies: $ `pip install -r requirements.txt`

* You can edit manually the `config.json` file
               or 
* run `./config.py` 

### Choosing your metrics
* Make sure that your metric is already monitored by cloudwatch
* Check the granularity of points (Default for monitoring in cloudwatch is 300s or 5 minutes)
* Type correctly the metric name and the namespace.
* Pay attetion in the name of your S3 bucket. 


![Diagrama](https://github.com/mariana-mendes/get-metrics-cloudwatch/blob/master/diagrama.png)
