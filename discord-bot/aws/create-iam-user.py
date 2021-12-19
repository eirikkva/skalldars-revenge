# Create IAM user for the discord bot
import boto3, os, json
from dotenv import load_dotenv

load_dotenv()

botname = os.getenv('botname')
policyName = os.getenv('botpolicyname')

iam = boto3.resource('iam')

policies = iam.policies.all()
for p in policies:
    if p.policy_name == policyName:
        break
else:
    p = None
    
if(p == None):
    print('Did not find bot policy - will not create user')
else:
    user = iam.create_user(
        UserName=botname,
        PermissionsBoundary=p.arn,
    )

    print('Created user {0}'.format(user.user_name))
