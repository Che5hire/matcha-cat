#Bot made by Che5hire#4179 (steamcommunity.com/id/che5hire on steam)
#~ try:
	#~ import discordrewrite
	#~ discord = discordrewrite
	#~ from discordrewrite.ext.commands import Bot
	#~ from discordrewrite.ext import commands
#~ except:
import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio, time, random, json, sys, datetime, configparser, os#, praw
modsloaded=[]
abouttext = '''Bot made by Che5hire#4179 (steamcommunity.com/id/che5hire on steam)
Version 0.5 (Alpha) "Is this the same bot? It doesn't even use the same library or anything."
This version of the bot is intended for the Kitten Squad discord server only, a more portable public bot will be made if there is high enough demand.
Expect matchmaking and tournament features in the near future

By using any of the commands or services supplied by this bot and related servers you're agreeing to the terms and conditions here: https://discordapp.com/developers/docs/legal
You also agree and acknowledge that any information supplied to the bot may be stored and used for services or functions supplied by any other servers I host. (I will not sell this information to 3rd parties.)'''
cfg = configparser.ConfigParser()
cfg.read('matchacat/matchacat.ini')

if cfg.getboolean("minecraft", "WhiteList"):
	import mcrcon
	rcon = mcrcon.MCRcon()

OwnerID = int(cfg.get('bot', 'OwnerID'))
bot = commands.Bot(command_prefix = '$', description=abouttext)

async def display_time():
	#This function is a loop that will update 'playing' to the server's current time every second.
	await bot.wait_until_ready()
	clocktime = ''
	try:
		while not bot.is_closed():
			if (time.strftime('%I:%M%p %Z', time.localtime()) != clocktime):
				clocktime = time.strftime('%I:%M%p %Z', time.localtime())
				await bot.change_presence(activity=discord.Game(name=time.strftime('%I:%M%p %Z', time.localtime())))
			await asyncio.sleep(2)
	except:
		e = sys.exc_info()[0]
		print(e)
@bot.event
async def on_ready():
	await reloadmods(modsloaded)
	print("ready!")
	if (cfg.get('bot', 'DisplayTime') != 'true'):
		await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name='$help'))
@bot.event
async def on_message(message):
	if (message.content.lower().find('shadman') != -1) and (message.content.lower().find('>shadman') == -1):
		await message.channel.send(message.channel, '```css\n>shadman```')
			
	if (not message.author.bot) and (str(message.channel).startswith('Direct Message with')):
		await message.channel.send('Commands via DM are currently not supported.')
	else:
		await bot.process_commands(message)
@bot.command(hidden=True)
async def mods(ctx):
	if ctx.message.author.id == OwnerID:
		await reloadmods(modsloaded)
		await ctx.send('Done')
	else:
		ctx.send('Only the bot owner (not the server owner) can use this command.')
async def reloadmods(modsloaded):
	if modsloaded != []:
		for mod in modsloaded:
			try:
				print('Unloading {}'.format(mod))
				bot.unload_extension("matchamods.{}".format(mod))
			except:
				e = sys.exc_info()[0]
				print(e)
				print("Failed to unload {}.".format(name))
	for file in os.listdir("matchamods"): #loads every cog in the matchamods folder
				if file.endswith(".py"):
					name = file[:-3]
					try:
						print("matchamods.{}".format(name))
						bot.load_extension("matchamods.{}".format(name))
					except:
						e = sys.exc_info()[0]
						print(e)
						print("Failed to load {}.".format(name))
					else:
						modsloaded += [name]
cfg.read('matchacat/matchacat.ini')
if (cfg.get('bot', 'DisplayTime') == 'true'):
	bot.loop.create_task(display_time())
DiscordToken = cfg.get('bot', 'BotToken')
bot.run(DiscordToken)
