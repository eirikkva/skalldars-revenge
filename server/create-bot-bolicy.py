import boto3, json, os
from dotenv import load_dotenv
load_dotenv()

policyName = os.getenv('botpolicyname')
iam = boto3.resource('iam')

# This policy allows starting and stopping instances if the user is tagged as owner
bot_policy_json = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "ec2:StartInstances",
                "ec2:StopInstances"
            ],
            "Resource": "arn:aws:ec2:*:*:instance/*",
            "Condition": {
                "StringEquals": {
                    "aws:ResourceTag/Owner": "${aws:username}"
                }
            }
        },
        {
            "Effect": "Allow",
            "Action": "ec2:DescribeInstances",
            "Resource": "*"
        }
    ]
}

policies = iam.policies.all()
for p in policies:
    if p.policy_name == policyName:
        print("Policy exists - will not create")
        break
else:
    p = None

if(p == None):
    print('Creating policy...')
    policy = iam.create_policy(
        PolicyName=policyName,
        Description='Enables aws users that are tagged as Owner to start and stop the EC2 instance. Intended for bots',
        PolicyDocument=json.dumps(bot_policy_json)
    ) 

    print(policy)
