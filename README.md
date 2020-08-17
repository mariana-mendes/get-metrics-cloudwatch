# get-metrics-cloudwatch


### Setup of a collecting instance
 
* Launch an EC2 instance. 
* Create a IAM Role 
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
* Attach your new policy to instance
* Access your instance (ssh etc)

Required 
install python
install aws cli
configure aws 
  
