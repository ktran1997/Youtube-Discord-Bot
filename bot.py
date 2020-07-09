import discord
import youtube_dl
import shutil
import os

from discord.ext import commands
from discord.utils import get

TOKEN = 'NzMwNTU5ODcyNzkzNTc1NjA0.XwZTqQ._EiseKBPdmKU8Kpl6HlQaYnswmA'
client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
	activity = discord.Game(name="with the API")
	await client.change_presence(status=discord.Status.idle, activity=activity)
	print('Bot online.')

@client.command(pass_context=True)
async def join(ctx):
	global voice
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild=ctx.guild)

	if voice and voice.is_connected():
		await voice.move_to(channel)
	else: 
		voice = await channel.connect()
	await ctx.send(f"joined {channel}")

@client.command(pass_context=True)
async def leave(ctx):
	channel = ctx.message.author.voice.channel
	voice = get(client.voice_clients, guild=ctx.guild)
	if voice and voice.is_connected():
		await voice.disconnect()
		await ctx.send(f"Left {channel}")

@client.command(pass_context=True, aliases=['c', 'erase'])
async def clear(ctx):
	queues.clear()
	print("Queues Cleared")
	await ctx.send("Queues are officailly cleared")
	return 

@client.command(pass_context=True, aliases=['a', 'activate'])
async def play(ctx, url:str):
	def check_queue():
		Queue_infile = os.path.isdir("./Queue")
		if Queue_infile is True:
			DIR = os.path.abspath(os.path.realpath("Queue"))
			length = len(os.listdir(DIR))
			still_q = length - 1
			try: 
				first_file = os.listdir(DIR)[0]
				print("testing 3")
			except:
				print("No more queued song(s)\n")
				queues.clear()
				return
			main_location = os.path.dirname(os.path.realpath(_file_))
			song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
			if length != 0:
				print("Song done, playing next in queue\n")
				print(f"Songs still in queue: {still_q}")
				song_there = os.path.isfile("song.mp3")
				if song_there:
					os.remove("song.mp3")
				shutil.move(song_path, main_location)
				for file in os.listdir("./"):
					if file.endswith(".mp3"):
						os.rename(file,'song.mp3')
				voice.play(discord.FFmpegPCMAudio("song.mp3"), after = lambda e: check_queue())
				voice.source = discord.PCMVolumeTransformer(voice.source)
				voice.source.volume = 0.07

			else: 
				queues.clear()
				return
		else: 
			queues.clear()
			print("No songs were queued before the ending of the last song\n")

	song_there = os.path.isfile("song.mp3")

	try: 
		if song_there:
			os.remove("song.mp3")
			queues.clear()
			print("Removed old song file")

	except PermissionError:
		print("trying to delete song file, but it's being played")
		await ctx.send("ERROR: Music playing")
		return 

	Queue_infile = os.path.isdir("./Queue")

	try: 
		Queue_folder = "./Queue"
		if Queue_infile is True: 
			print("Removed old Queue Folder")
			shutil.rmtree(Queue_folder)

	except: 
		print("No old Queue folder")

	await ctx.send("Getting everything ready now")

	voice = get(client.voice_clients, guild=ctx.guild)

	ydl_opts = {
		'format' : 'bestaudio/best',
		'quiet' : True, 
		'postprocessors' : [{
			'key' : 'FFmpegExtractAudio', 
			'preferredcodec' : 'mp3', 
			'preferredquality' : '192',
		}],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print("Downloading audio now\n")
		ydl.download([url])

	for file in os.listdir("./"):
		if file.endswith(".mp3"):
			name = file
			print(f"Renamed File: {file}\n")
			os.rename(file, "song.mp3")
	voice.play(discord.FFmpegPCMAudio("song.mp3"), after = lambda e: check_queue())
	voice.source = discord.PCMVolumeTransformer(voice.source)
	voice.source.volume = 0.07

	nname = name.rsplit("-", 2)
	await ctx.send(f"Playing: {nname[0]}")
	print("playing\n")

@client.command(pass_context=True, aliases=['s', 'stop'])
async def pause(ctx):
	voice = get(client.voice_clients, guild=ctx.guild)

	if voice and voice.is_playing():
		print("Music paused")
		voice.pause()
		await ctx.send("Music paused")
	else: 
		print("Music not playing failed pause")
		await ctx.send("Music not playing failed pause")

@client.command(pass_context=True, aliases=['p', 'proceed'])
async def resume(ctx):
	voice = get(client.voice_clients, guild=ctx.guild)

	if voice and voice.is_paused():
		print("Resumed music")
		voice.resume()
		await ctx.send("Resumed music")
	else:
		print("Music is not paused")
		await ctx.send("Music is not paused")

@client.command(pass_context=True, aliases=['d', 'dodge'])
async def skip(ctx):
	voice = get(client.voice_clients, guild=ctx.guild)

	queues.clear()

	if voice and voice.is_playing():
		print("Music skipped")
		voice.stop()
		await ctx.send("Music skipped")
	else: 
		print("No music playing failed to skip")
		await ctx.send("No music playing failed to skip")

queues = {}

@client.command(pass_context=True, aliases=['n', 'next'])
async def queue(ctx, url:str):
	Queue_infile = os.path.isdir("./Queue")
	if Queue_infile is False: 
		os.mkdir("Queue")
	DIR = os.path.abspath(os.path.realpath("Queue"))
	q_num = len(os.listdir(DIR))
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
		'format' : 'bestaudio/best',
		'quiet' : True, 
		'outmpl' : queue_path, 
		'postprocessors' : [{
			'key' : 'FFmpegExtractAudio',
			'preferredcodec' : 'mp3',
			'preferredquality' : '192'
		}],
	}

	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		print("Downloading audio now\n")
		ydl.download([url])
	await ctx.send("Adding song " + str(q_num) + " to the queue")

	print("Song added to queue\n")



client.run(TOKEN)
