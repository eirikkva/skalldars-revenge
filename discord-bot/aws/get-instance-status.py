import os, boto3
from dotenv import load_dotenv

load_dotenv()

ec2 = boto3.resource('ec2')

sshkey = os.getenv('ec2keyname')
botname = os.getenv('botname')

existingInstances = list(ec2.instances.filter(Filters=[{'Name':'tag:botname', 'Values': [botname]}]))
instance = existingInstances[0]

status = instance.state['Name']

print('Status on {0} is : {1}'.format(botname, status))

if(status == 'running'):
    print('ssh -i {0}.pem ec2-user@{1}'.format(sshkey, instance.public_dns_name))
else:
    print('Not in running state you need to start if you want to get ssh connection info')



    
