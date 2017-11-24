# AWS EC2 Event Notification to Slack

## Advance preparation

```
$ pip install lambda-uploader awscli
$ aws configure --profile <profile>
```

## File Structure

```
.
├── README.md
├── event.json
├── lambda.json
├── lambda_function.py
└── requirements.txt
```

Main lambda function is `lambda_function.py` with Python 3.6.

- lambda.json

```
"role": "arn:aws:iam::xxxxxxxxxxxx:role/lambda-check-events-to-slack",
```

* this `role` is attached a policy as follows:

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
                "ec2:Describe*"
            ],
            "Resource": "*"
        }
    ]
}
```

* and trusted entity : `lambda.amazonaws.com`

## Upload to AWS Lambda

```
$ lambda-uploader --profile <profile>

Î» Building Package
Î» Uploading Package
Î» Fin
```

## Confirm
![AWS Lambda Console](http://i.imgur.com/G4p85eb.png)

## Save & Test

![Slack](http://i.imgur.com/Eme2uw7.png)

It's good !

THX ♪
