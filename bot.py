
import asyncio
import discord
import SerchAnime
from discord.ext import commands
import Config
import Youtube
import pafy
import Youtube
from collections import defaultdict, deque
# *---About pafy ---*
FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

YOUTUBE_URL_HEADER = "https: // www.youtube.com/watch?v="


# *---About Discord.py---*
TOKEN = Config.DISCORD_TOKEN
Bot = commands.Bot(command_prefix="$")

# *---Others---*
OPname = ""
helpinfo = """
*コマンド一覧*
```・$join :ボイスチャンネルに接続します
・$leave :ボイスチャンネルを退出します
・$serchAnime "検索するアニメ名" : アニメを検索をして情報を入力します
・$play "キーワード" : キーワードをyoutubeで検索しボイスチャンネルで再生します
                      キーワードに--aと入力すれば直前に検索したアニメのOPを再生します
・$stop :音楽の再生を止めます
・$command :コマンドリストを表示します```"""

titles = []
queue_dict = defaultdict(deque)


@Bot.event
async def on_ready():
    print(f'We have logged in as {Bot.user}')
    queueclear()


@Bot.event
async def on_message(message):
    if message.author == Bot.user:
        return

    await Bot.process_commands(message)


@ Bot.command()
async def command(ctx):
    await ctx.send(helpinfo)


@ Bot.command()
async def serchAnime(ctx, s):
    resetAnimeName()
    print("アニメを検索します")
    await ctx.send("アニメを検索します")
    data, titles = SerchAnime.serchAnime(s)
    [await ctx.send(f"""・{i+1}:
    {c}""") for i, c in enumerate(data)]
    if len(data) == 0:
        await ctx.send("検索出来ませんでした,コマンドを入力しなおしてください")
        return
    await ctx.send("検索結果の候補はこちらになります")
    await ctx.send("探していたアニメの番号を入力してください")

    def check(m):
        if m.content.isdigit():

            return m.author == ctx.message.author and m.channel == ctx.message.channel
        return False

    try:
        msg = await Bot.wait_for("message", check=check, timeout=50)
    except asyncio.TimeoutError:
        await ctx.send("タイムアウトしました。再度検索をお願いします")
    else:
        selectNum = int(msg.content)
        await ctx.send(f"はい、{selectNum}ですね。情報を再表示します")
        await ctx.send(f"""・{selectNum}:
        {data[selectNum-1]}""")

        await ctx.send("opを再生しますか？ 再生する場合は👍を押してください")

        def check2(reaction, m):
            return m == ctx.message.author and str(reaction.emoji) == "👍"

        try:
            msg2 = await Bot.wait_for("reaction_add", check=check2, timeout=40,)
        except asyncio.TimeoutError:
            await ctx.send("かしこまりました、またお声掛けください。")
        else:

            print("アニメ名"+changeAnimeName(titles[selectNum-1] + " OP"))
            await ctx.send("OPを検索して再生します $play --a と入力してください")


def enuqueue(voice_client, guild, source):
    queue = queue_dict[guild.id]
    queue.append(source)
    if not voice_client.is_playing():
        print("再生を開始")
        playAud(voice_client, queue)


def playAud(voice_client, queue):
    if not queue or voice_client.is_playing():
        return
    source = queue.popleft()
    titles.pop(0)
    voice_client.play(source, after=lambda e: playAud(voice_client, queue))


@ Bot.command()
async def serchMusic(ctx):

    print("音楽を検索します:")
    await ctx.send("音楽を検索します")


@ Bot.command()
async def play(ctx, s):
    await isConnect(ctx)
    if len(titles) == 0:
        print(f"音楽を再生します:{s}")
        if s == "--a":
            await isAnime(ctx)

            audio, title, url = PlayAnimeSongs(ctx)
            await ctx.send(url)
            titles.append(title)
            print(titles)
            enuqueue(ctx.guild.voice_client, ctx.guild,
                     discord.FFmpegPCMAudio(audio))
            await ctx.send(f"{title}を再生します")
        else:

            audio, title, url = PlaySongs(ctx, s)
            await ctx.send(url)
            titles.append(title)
            print(titles)
            enuqueue(ctx.guild.voice_client, ctx.guild,
                     discord.FFmpegPCMAudio(audio))
            await ctx.send(f"{title}を再生します")

    else:
        if s == "--a":
            await isAnime(ctx)

            audio, title, url = PlayAnimeSongs(ctx)
            await ctx.send(url)
            titles.append(title)
            print(titles)
            enuqueue(ctx.guild.voice_client, ctx.guild,
                     discord.FFmpegPCMAudio(audio))
            await ctx.send(f"""キューに追加しました
            ```{titles}```""")

        else:

            audio, title, url = PlaySongs(ctx, s)
            await ctx.send(url)
            titles.append(title)
            print(titles)
            enuqueue(ctx.guild.voice_client, ctx.guild,
                     discord.FFmpegPCMAudio(audio))
            await ctx.send(f"""キューに追加しました
            ```{titles}```""")


async def isConnect(ctx):

    if ctx.author.voice is None:
        await ctx.send("接続されていません")
    else:
        voice_client = discord.utils.get(
            Bot.voice_clients, guild=ctx.guild)
        if voice_client:
            await ctx.send("すでに接続されています")
        else:
            await ctx.author.voice.channel.connect()


async def isAnime(ctx):
    if OPname == "":
        print("アニメが検索されていません")
        await ctx.send("アニメが指定されていません '$serchAnime アニメ名'を入力しアニメを検索してください")
        return
    else:
        print(OPname)
        await ctx.send("検索したアニメのOPを再生します")


def PlayAnimeSongs(ctx):
    print("アニメ:"+OPname)
    id, title = Youtube.serchYoutube(OPname)
    url = "https://www.youtube.com/watch?v=" + id
    song = pafy.new(id)
    audio = song.getbestaudio()
    return audio.url, title, url


def PlaySongs(ctx, s):
    id, title = Youtube.serchYoutube(s)
    url = "https://www.youtube.com/watch?v=" + id
    song = pafy.new(id)
    audio = song.getbestaudio()
    return audio.url, title, url


@ Bot.command()
async def GetURL(ctx, s):
    url = "https://www.youtube.com/watch?v="+Youtube.serchYoutube(s)
    await ctx.send(url)


@ Bot.command()
async def join(ctx):
    await ctx.author.voice.channel.connect()


@ Bot.command()
async def leave(ctx):
    await ctx.voice_client.disconnect()


@ Bot.command()
async def stop(ctx):
    if not ctx.guild.voice_client.is_playing():
        await ctx.channel.send("再生していません。")
        return
    print("再生中の音楽を停止します")
    ctx.guild.voice_client.stop()
    await ctx.send("再生中の音楽を停止します")


@ Bot.command()
async def skip(ctx):
    print("再生中の音楽をスキップします")
    await ctx.send("再生中の音楽をスキップします")


@ Bot.command()
async def queue(ctx):
    print("queue")
    await ctx.send("キューを表示します")


def changeAnimeName(s):
    global OPname
    OPname = s
    return OPname


def resetAnimeName():
    global OPname
    OPname = ""


def queueclear():
    titles.clear()


Bot.run(TOKEN)
