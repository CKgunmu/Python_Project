import os
import ssl
import shutil
import youtube_dl
import discord
from discord.ext import commands
from discord.utils import get
from google_images_download import google_images_download

BOT_PREFIX = '/'
ssl._create_default_https_context = ssl._create_unverified_context
TOKEN = '봇 '

bot = commands.Bot(command_prefix=BOT_PREFIX)

@bot.event
async def on_ready():
    print("Logged in as: " + bot.user.name + "\n")


#discord voice channel in&out
@bot.command(pass_context=True, aliases=['j', 'joi'])
async def join(ctx):
    global voice
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")

@bot.command(pass_context=True, aliases=['l', 'lea'])
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")

#bot message delete
@bot.command(pass_context=True, aliases=['bmd'])
async def bot_message_delete(ctx, amount=20):
    await ctx.channel.purge(limit=amount)


#bot embed
@bot.command(pass_context=True, aliases=['!help'])
async def helped(ctx):
    em = discord.Embed(title="설명문",color=0x00ff6e,
                       description="""
                        url: 주소\n
                        /join,  j               봇을 통화방에 추가\n
                        /leave, l               봇을 통화방에서 제거\n
                        /play url, p url        봇이 노래를 틀어준다\n
                        /stop, s                모든노래가 삭제됨\n
                        /pause, pa              재생중인 노래 정지\n
                        /resume, r              멈춰있던 노래 재생\n
                        /queue, qu              노래 예약\n
                        /next, n                스킵과 같은기능 다음곡으로 넘어감\n
                        /picture_download, /pd   원하는 검색어의 상위20개 데이터를 찾음\n
                        /picture_point, /pp      원하는 사진번호를 입력 위에서부터 아래로 0~99\n
                        /picture_list, /plist    다운받은 사진들의 목록을 보여줌\n
                        /picture_delete, /pdel   사진목록을 전부 삭제\n
                       """)
    await ctx.channel.send(embed=em)

#music play
@bot.command(pass_context=True, aliases=['p', 'pla'])
async def play(ctx, url: str):

    def check_queue():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is True:
            DIR = os.path.abspath(os.path.realpath("Queue"))
            length = len(os.listdir(DIR))
            still_q = length - 1

            try:
                first_file = os.listdir(DIR)[0]
            except:
                print("No more queue song(s)\n")
                queues.clear()
                return
            main_location = os.path.dirname(os.path.realpath(__file__))
            song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
            if length != 0:
                print("Song done, playing next queued\n")
                print(f"Songs still in queue: {still_q}")
                song_there = os.path.isfile("song.mp3")
                if song_there:
                    os.remove("song.mp3")
                shutil.move(song_path, main_location)
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        os.rename(file, 'song.mp3')

                voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
                voice.source = discord.PCMVolumeTransformer(voice.source)
                voice.source.volume = 0.07

            else:
                queues.clear()
                return
        else:
            queues.clear()
            print("No Songs were queued before the ending of the last song\n")

    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
            queues.clear()
            print("Removed old song file")
    except PermissionError:
        print("Trying to delete song file, but it's being played")
        await ctx.send("ERROR: Music palying")
        return

    Queue_infile = os.path.isdir("./Queue")
    try:
        Queue_folder = "./Queue"
        if Queue_infile is True:
            print("Removed old Queue Folder")
            shutil.rmtree(Queue_folder)
    except:
        print("No old Queue Folder")


    await ctx.send("Getting everything ready now")

    voice = get(bot.voice_clients, guild=ctx.guild)

    ydl_opts = {
        'format':'bestaudio/best',
        'quiet' : True,
        'postprocessors' : [{
            'key' : 'FFmpegExtractAudio',
            'preferredcodec':'mp3',
            'preferredquality':'192',
        }],
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = str(file)
            print(f"Renamed File: {file}\n")
            os.rename(file, "song.mp3")

    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    await ctx.send(f"Playing Song")
    print("playing\n")

@bot.command(pass_context=True, aliases=['pa', 'pau'])
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        print("Resumed music")
        voice.pause()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")

@bot.command(pass_context=True, aliases=['r', 'res'])
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_paused():
        print("Resumed music")
        voice.resume()
        await ctx.send("Resumed music")
    else:
        print("Music is not paused")
        await ctx.send("Music is not paused")

@bot.command(pass_context=True, aliases=['s', 'sto'])
async def stop(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    queue.clear()
    queue_infile = os.path.isdir("./Queue")
    if queue_infile is True:
        shutil.rmtree("./Queue")

    if voice and voice.is_playing():
        print("Music stopped")
        voice.stop()
        await ctx.send("Music stopped")
    else:
        print("No music playing failed to stop")
        await ctx.send("No music playing failed to stop")

queues = {}

@bot.command(pass_context=True, aliases=['q', 'que'])
async def queue(ctx, url:str):
    Queue_infile = os.path.isdir("./Queue")
    if Queue_infile is False:
        os.mkdir("Queue")
    DIR = os.path.abspath(os.path.realpath("Queue"))
    q_num =  len(os.listdir(DIR))
    q_num += 1
    add_queue = True
    while add_queue:
        if q_num in queues:
            q_num += 1
        else:
            add_queue = False
            queues[q_num] = q_num

    queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")

    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'outtmpl':queue_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],


    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        print("Downloading audio now\n")
        ydl.download([url])

    await ctx.send("Adding song " + str(q_num) + " to the queue")
    print("Song added to queue\n")


@bot.command(pass_context=True, aliases=['n', 'nex'])
async def next(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        print("Playing next song")
        voice.stop()
        await ctx.send("Next Song")
    else:
        print("No music playing failed to play next song")
        await ctx.send("No music playing failed")


#picture download & print
picture_dir = os.path.abspath(os.path.realpath("Image/"))
print(picture_dir)
@bot.command(pass_context=True, aliases=['pd'])
async def picture_download(ctx, Keyword:str):
    i=0
    file = os.listdir(picture_dir)
    for a in file: i+=1
    if i >= 100:
        await ctx.send("Too many files Please use after deleting the file Use this command: ")
        print("file download error")
        return

    dir = picture_dir
    response = google_images_download.googleimagesdownload()
    arguments = {
        "keywords" : Keyword,
        "limit" : 20,
        "print_urls":True,
        "no_directory" : True,
        "output_directory":dir
    }
    paths = response.download(arguments)
    print(paths)

@bot.command(pass_context=True, aliases=['pp'])
async def picture_point(ctx, point:int):
    if point > 100:
        await ctx.send("Out of range\nPlease enter a number below 100")
        return

    filename = os.listdir(picture_dir)
    await ctx.send(file=discord.File(picture_dir+"/"+filename[point]))
    await ctx.send(filename[point])

@bot.command(pass_context=True, aliases=['plist'])
async def picture_list(ctx):
    filename = os.listdir(picture_dir)
    filename.sort()
    for name in filename:
        await ctx.send(name)

@bot.command(pass_context=True, aliases=['pdel'])
async def picture_delete(ctx):
    filename = os.listdir(picture_dir)
    for name in filename:
        os.remove(picture_dir+"/"+name)
        await ctx.send(name + " delete")

bot.run(TOKEN)
