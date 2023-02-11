import discord
import requests
from datetime import datetime
import configparser
from discord.ext import tasks

config = configparser.ConfigParser()
config.read('config.ini')

ipUrlApi = 'https://api.ipify.org'
discordIpChannelId = int(config['DEFAULT']['ChannelId'])
secret = config['DEFAULT']['ClientSecret']

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

ipAnnouncementText = f"Aktuelle Minecraft IP: "
ipMinecraftPort = ":25565"

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    print("Starting scheduled task")        
    on_schedule_ip.start()
     
def get_new_ip():
        currentIp = requests.get(ipUrlApi).text
        return currentIp
    
@tasks.loop(minutes=5)
async def on_schedule_ip():
    channel = client.get_channel(discordIpChannelId)
    newIp = ipAnnouncementText + get_new_ip() + ipMinecraftPort
    lastIp = newIp
    async for message in channel.history(limit=1):
        print("Reading last message of channel")
        lastIp = message.content
    
    print(lastIp)
    if(newIp != lastIp):
        print("Updating IP")
        print(newIp)
        await channel.send(newIp)
    else:
        print("No update")
    
client.run(secret)
