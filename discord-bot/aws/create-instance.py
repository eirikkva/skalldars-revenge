import boto3, os
from dotenv import load_dotenv

load_dotenv()

ec2 = boto3.resource('ec2')

ec2KeyName = os.getenv('ec2keyname')
ec2KeyFileName = '{0}.pem'.format(ec2KeyName)
if(os.path.isfile(ec2KeyFileName)!= True):
    createEc2KeyPair(ec2KeyFileName, ec2KeyName)

# create a new EC2 instance
botname = os.getenv('botname')
existingInstances = list(ec2.instances.filter(Filters=[{'Name':'tag:botname', 'Values': [botname]}]))

if(len(existingInstances) > 0):
    state = existingInstances[0].state
    print('EC2 instance for {0} already exists and is in state: {1}'.format(botname, state))
    print(existingInstances[0])
else:
    print('Creating EC2 instance for the bot {0}'.format(botname))
    instances = ec2.create_instances(
        ImageId='ami-06bfd6343550d4a29',
        MinCount=1,
        MaxCount=1,
        InstanceType='t3.micro',
        TagSpecifications=[
            {
                'ResourceType': 'instance',
                'Tags': [
                    {
                        'Key': 'botname',
                        'Value': botname
                    },
                ]
            }
        ],
        SecurityGroups=[
        'discord-bot',
        ],
        KeyName='{0}'.format(ec2KeyName)
    )

    instance = instances[0]

    # Wait for the instance to enter the running state
    instance.wait_until_running()

    # Reload the instance attributes
    instance.load()
    print('ssh -i {0}.pem ec2-user@{1}'.format(ec2KeyName, instance.public_dns_name))


def createEc2KeyPair(outFileName, keyName):
    # create a file to store the key locally
    outfile = open(outFileName,'w')

    # call the boto ec2 function to create a key pair
    key_pair = ec2.create_key_pair(KeyName='{0}'.format(keyName))

    # capture the key and store it in a file
    KeyPairOut = str(key_pair.key_material)
    print(KeyPairOut)
    outfile.write(KeyPairOut)