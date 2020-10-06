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
                "ec2:DescribeTags",
                "elasticloadbalancing:DescribeTags",
                "elasticloadbalancing:DescribeLoadBalancerPolicyTypes",
                "cloudwatch:GetMetricStatistics",
                "cloudwatch:ListMetrics",
                "elasticloadbalancing:DescribeLoadBalancerAttributes",
                "elasticloadbalancing:DescribeLoadBalancers",
                "autoscaling:DescribeScalingActivities",
                "autoscaling:DescribeAutoScalingGroups",
                "elasticloadbalancing:DescribeLoadBalancerPolicies",
                "elasticloadbalancing:DescribeInstanceHealth"
            ],
            "Resource": "*"
          }
              ]
       }```
     
### Inital config 
* Clone the repo:  $ `git clone https://github.com/mariana-mendes/get-metrics-cloudwatch.git && cd get-metrics-cloudwatch` 
* Install dependencies: $ `pip install -r requirements.txt`
* Configuring Collector: $ `./config.py` 

### Choosing your metrics
* Make sure that your metric is already monitored by cloudwatch
* Check the granularity of points (Default for monitoring in cloudwatch is 300s (5 minutes))
* Type correctly the metric name and the namespace.
* Pay attetion in the name of your S3 bucket. 

Make sure that your config looks like this:
   ```
  {
    "metricsDescription": [
        {
            "metricName": "CPUUtilization",
            "namespace": "AWS/EC2",
            "dimension": "InstanceId"
        },
        {
            "metricName": "RequestCount",
            "namespace": "AWS/ApplicationELB",
            "dimension": "LoadBalancer"
        },
        {
            "metricName": "GroupTotalCapacity",
            "namespace": "AWS/AutoScaling",
            "dimension": "AutoScalingGroupName"
        }
    ],
    "endTime": "2020-09-15T20:00:02.819519",
    "period": "300",
    "startTime": "2020-09-15T19:00:02.819532",
    "storage": {
        "InstanceId": "folder-in-my-bucket",
        "LoadBalancer": "also-local-folder",
        "AutoScalingGroupName": "folder-name"
    },
    "aws-config": {
        "region": "us-east-1",
        "bucket": "my-bucket-name"
    }
}
   ```



![Diagrama](https://github.com/mariana-mendes/get-metrics-cloudwatch/blob/master/diagrama.png)
