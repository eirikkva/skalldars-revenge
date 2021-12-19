import discord, os, boto3, socket, traceback
from dotenv import load_dotenv

load_dotenv()

client = discord.Client()

ec2 = boto3.resource('ec2')

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.lower().startswith('help'):
        await message.channel.send('I am Yuri Skallagrimson! \n Available commands: "start", "stop" "state" and "help"')

    # Find the EC2 instance with a tag that corresponds to the guild id (discord server)
    instances = list(ec2.instances.filter(Filters=[{'Name':'tag:guild', 'Values': [str(message.channel.guild.id)]}]))
    print('Found guild id math on ' + str(instances[0]) + ' (' + str(len(instances)) + ' matching instances)')
    instance = instances[0]

    if message.content.lower().startswith('start'):
        if startInstance(instance):
            await message.channel.send('I will start {0} with Password: {1} \n Use "state" to verify. '.format(os.getenv('OPENRA_NAME'),os.getenv('OPENRA_PASSWORD')))
        else:
            await message.channel.send('Crrritical error - Yuri could not start {0}'.format(os.getenv('OPENRA_NAME')))

    if message.content.lower().startswith('stop'):
        if shutDownInstance(instance):
            await message.channel.send('You want to stop {0}!??!? Okay,okay I stop'.format(os.getenv('OPENRA_NAME')))
        else:
            await message.channel.send('Something is wrong, I have problems shutting down {0}'.format(os.getenv('OPENRA_NAME')))

    if message.content.lower().startswith('state'):
         await message.channel.send('{0} is: {1}'.format(os.getenv('OPENRA_NAME'), getInstanceState(instance)))

def shutDownInstance(instance):
    try:
        instance.stop()
        return True
    except: 
        print(traceback.format_exc())
        return False

def startInstance(instance):
    try:
        instance.start()
        return True
    except:
        print(traceback.format_exc())
        return False

def getInstanceState(instance):
    aws_state = instance.state
    if (aws_state['Name'] == 'running'):
        return getPortState(instance.public_ip_address, 1234)
    else:
        return aws_state['Name']

def getPortState(ip, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(3.0)
    ready = sock.connect_ex((ip, port))
    if ready == 0:
        return 'ready at ' + ip 
    else:
        return 'starting, please wait or I put you in Gulag'


client.run(os.getenv('DISCORD_TOKEN'))