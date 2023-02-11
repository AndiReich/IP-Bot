import discord
import requests
import time
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

ipUrlApi = 'https://api.ipify.org'
discordIpChannelId = int(config['DEFAULT']['ChannelId'])
secret = config['DEFAULT']['ClientSecret']
lastIp = ""

intents = discord.Intents.all()
intents.message_content = True
client = discord.Client(intents=intents)

ipAnnouncementText = f"Aktuelle Minecraft IP: "
ipMinecraftPort = ":25565"

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    lastIp = get_new_ip()
    channel = client.get_channel(discordIpChannelId)
    print(f"Posting on channel: {discordIpChannelId}")
    await channel.send(ipAnnouncementText + lastIp + ipMinecraftPort)
    print("Starting endless loop")
    while(True):
        newIp = get_new_ip()
        if(lastIp != newIp):
            print(ipAnnouncementText + lastIp + ipMinecraftPort)
            await channel.send(ipAnnouncementText + lastIp + ipMinecraftPort)
            lastIp = newIp
        else:
            print("No update")
        time.sleep(120)
     
def get_new_ip():
        currentIp = requests.get(ipUrlApi).text
        print(f"Got IP: {currentIp}")
        return currentIp

client.run(secret)
