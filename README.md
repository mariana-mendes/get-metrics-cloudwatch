# get-metrics-cloudwatch


### Setup instance
 
* Launch an EC2 instance. 
* Create an IAM Role 
    * Create a policy: 
      Using json editor, your policy should look like this
      ```{
          "Version": "2012-10-17",
          "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": [
                "autoscaling:DescribeAutoScalingInstances",
                "cloudwatch:PutMetricData",
                "cloudwatch:GetMetricData",
                "autoscaling:DescribeScalingActivities",
                "ec2:DescribeTags",
                "autoscaling:DescribeAutoScalingGroups",
                "cloudwatch:GetMetricStatistics",
                "cloudwatch:ListMetrics"
            ],
            "Resource": "*"
        }]}```
     
### Inital config 
* Clone the repo:  $ `git clone https://github.com/mariana-mendes/get-metrics-cloudwatch.git && cd get-metrics-cloudwatch` 
* Install dependencies: $ `pip install -r requirements.txt`
* Configuring Collector: $ `./config.py` 

### Choosing your metrics
* Make sure that your metric is already monitored by cloudwatch
* Check the granularity of points (Default for monitoring in cloudwatch is 300s or 5 minutes)
* Type correctly the metric name and the namespace.
* Pay attetion in the name of your S3 bucket. 

Make sure that your config looks like this:
   ```
   { 
        "metricsDescription": [
           {
             "metricName": "CPUUtilization",
             "namespace": "AWS/EC2"
           }
         ],
        "instancesDescription": [],
        "endTime": "2020-09-02T18:00:05.064378",
        "period": "300",
        "startTime": "2020-09-02T15:00:05.064401" 
   }
   ```



![Diagrama](https://github.com/mariana-mendes/get-metrics-cloudwatch/blob/master/diagrama.png)
