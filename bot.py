import discord
import SerchAnime
from discord.ext import commands
import json
import Config

TOKEN = Config.DISCORD_TOKEN


Bot = commands.Bot(command_prefix="!")


@Bot.event
async def on_ready():
    print(f'We have logged in as {Bot.user}')


@Bot.event
async def on_message(message):
    if message.author == Bot.user:
        return

    if message.content.startswith('!!'):
        await message.channel.send('Hello!,CanIhelp?')

    await Bot.process_commands(message)


@Bot.command()
async def serchAnime(ctx, s):
    print("アニメを検索します")
    await ctx.send("アニメを検索します")
    data = str(SerchAnime.serchAnime(s))
    print(data)
    await ctx.send(data)
    await ctx.send("こちらのアニメでよろしいですか？")


@ Bot.command()
async def serchMusic(ctx):
    print("音楽を検索します")
    await ctx.send("音楽を検索します")


@ Bot.command()
async def play(ctx):
    print("音楽を再生します")
    await ctx.send("音楽を再生します")


@ Bot.command()
async def stop(ctx):
    print("再生中の音楽を停止します")
    await ctx.send("再生中の音楽を停止します")


@ Bot.command()
async def skip(ctx):
    print("再生中の音楽をスキップします")
    await ctx.send("再生中の音楽をスキップします")


@ Bot.command()
async def queue(ctx):
    print("queue")
    await ctx.send("queue")


Bot.run(TOKEN)
