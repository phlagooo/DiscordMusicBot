import discord
from discord.ext import commands
from youtube import Yt
from music_player import Music_player
import asyncio
import os

def get_token():
    with open('../DiscordBot2Token.txt', 'r') as f:
        token = f.readline()
    return token

def setup():
    intents = discord.Intents.default()
    intents.message_content = True
    return commands.Bot(command_prefix='>', intents=intents)

token = get_token()
bot = setup()
music_player = Music_player()
now_playing_msg = None
same_song_count = 1

# Cleanup
for f in os.listdir():
    if f.endswith('.webm'):
        os.remove(f)
        print(f'Removed {f}')

# TEST
@bot.command()
async def ping(ctx):
    print(ctx)
    await ctx.send('pong')

# Music
@bot.command(name='play', help='Plays a song from YouTube')
async def play(ctx, url):
    global now_playing_msg
    global same_song_count
    if ctx.voice_client is None:
        await join(ctx)
    
    # If currently playing song, add as next in queue
    if ctx.voice_client.is_playing():
        music_player.add_as_next_song(url)
        yt = await Yt.from_url(url, loop=bot.loop, stream=True)
        await ctx.send(f'Added "{yt.title}" as next in queue')
        return
        
    if music_player.previous_song[1] == None:
        music_player.previous_song[1] = url

    async with ctx.typing():
        player = await Yt.from_url(url, loop=bot.loop, stream=True)
        ctx.voice_client.play(player, after=lambda e: asyncio.run_coroutine_threadsafe(play_next_song(ctx), bot.loop))

    if music_player.loop and (now_playing_msg is not None) and music_player.previous_song[1] == url:
        same_song_count += 1
        post = "nd" if same_song_count == 2 else "rd" if same_song_count == 3 else "th"
        now_playing_msg = await now_playing_msg.edit(content=f'Now playing: {player.title} for the {same_song_count}{post} time')
    else:
        now_playing_msg = await ctx.send(f'Now playing: {player.title}')
        same_song_count = 1

async def play_next_song(ctx):
    if music_player.loop:
        await play(ctx, music_player.get_previous_song())
    elif music_player.has_next():
        await play(ctx, music_player.get_next_song())
    else:
        await ctx.send('Queue is empty')
    

@bot.command(name='skip', help='Skips the current song')
async def skip(ctx):
    ctx.voice_client.stop()
    music_player.toggle_loop()
    await ctx.send('Skipped')
    await play_next_song(ctx)

@bot.command(name='clear', help='Clears the queue')
async def clear(ctx):
    music_player.clear_queue()
    await ctx.send('Queue cleared')

@bot.command(name='queue', help='Shows the queue')
async def queue(ctx):
    if len(music_player.queue) == 0:
        await ctx.send('Queue is empty')
    else:
        for i, song in enumerate(music_player.queue):
            yt = await Yt.from_url(song, loop=bot.loop, stream=True)
            await ctx.send(f'{i+1}: {yt.title}')

@bot.command(name='loop', help='Toggles loop')
async def loop(ctx):
    music_player.toggle_loop()
    await ctx.send(f'Looping: {music_player.loop}')

@bot.command(name='add', help='Adds a song to the queue')
async def add(ctx, url):
    music_player.add_song(url)
    yt = await Yt.from_url(url, loop=bot.loop, stream=True)
    await ctx.send(f'Added "{yt.title}" to the queue')

@bot.command(name='prev', help='Shows the queue')
async def prev(ctx):
    if music_player.get_previous_song() is None:
        await ctx.send('No previous song')
    else:
        await play(ctx, music_player.get_previous_song())

@bot.command(name='join', help='Join the voice channel you are in')
async def join(ctx):
    # Check if the user is in a voice channel
    if ctx.author.voice is None:
        await ctx.send("You are not in a voice channel.")
        return

    # Get the voice channel of the user
    voice_channel = ctx.author.voice.channel

    # If the bot is already in a voice channel, move to the new channel
    if ctx.voice_client is not None:
        return await ctx.voice_client.move_to(voice_channel)

    # Connect to the voice channel
    await voice_channel.connect()

@bot.command(name='leave', help='Leave the voice channel')
async def leave(ctx):
    # Check if the bot is in a voice channel
    if ctx.voice_client is None:
        await ctx.send("I am not in a voice channel.")
        return

    # Disconnect from the voice channel
    await ctx.voice_client.disconnect()

bot.run(token)