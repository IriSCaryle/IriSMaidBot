import discord
import json
TOKEN = ""
COMMANDLIST_PATH = ""

client = discord.Client()


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('!!'):
        await message.channel.send('Hello!,CanIhelp?')

client.run('your token here')
