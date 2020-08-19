# :construction: under construction :construction: :construction_worker:

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
  
  
### Inital config 
`git clone https://github.com/mariana-mendes/get-metrics-cloudwatch.git && cd get-metrics-cloudwatch` 

* You can edit manually the `config.json` file
               or 
* run `./config.py` 

![Diagrama](https://github.com/mariana-mendes/get-metrics-cloudwatch/blob/master/diagrama.png)
