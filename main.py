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
import mcrcon, asyncio, time, random, json, sys, datetime, configparser, os#, praw
modsloaded=[]
abouttext = '''Bot made by Che5hire#4179 (steamcommunity.com/id/che5hire on steam)
Version 0.5 (Alpha) "Is this the same bot? It doesn't even use the same library or anything."
This version of the bot is intended for the Kitten Squad discord server only, a more portable public bot will be made if there is high enough demand.
Expect matchmaking and tournament features in the near future

By using any of the commands or services supplied by this bot and related servers you're agreeing to the terms and conditions here: https://discordapp.com/developers/docs/legal
You also agree and acknowledge that any information supplied to the bot may be stored and used for services or functions supplied by any other servers I host. (I will not sell this information to 3rd parties.)'''

'''helptext = \'''(By using any of the commands below (besides $help and $about) you are agreeing to any terms and conditions I list in the $about command. Unless stated otherwise assume the command starts with a $)
help [-c]
	PMs you this message, -c will print this message to the channel you typed it in.

about
	Information about the bot itself and not the commands such as: Version number, author, etc.

adduser __USERNAME__
	Associates a username from pokemon showdown to your discord account for the $whois command. Keep in mind that entering this command will overwrite your previous username. This will be used for future commands and more websites will come soon.

whitelist [-r] __YOURMINECRAFTUSERNAME__
	Adds your username to our server's whitelist, adding -r without specifying a username will remove the name your registered.

whois [-OPTIONS] __NAME__
	Prints the discord user's minecraft name if it has been registered using 'whitelist', -mc lets you find a discord name using their Minecraft username
	-mc: finds a discord username using their minecraft username.
	-sd: finds a discord username using their showdown username.
	
sprite __POKEMON__
	Posts a sprite of a shiny pokemon on the channel using the sprite library
	
rep [DISCORDNAME]
	Tells you how many 💮 reactions have been added to a users posts.
	
colour __COLOUR__
OR
color __COLOR__
	Changes your name's colour, check matchacat for a list of colours..''' #This was phased out in favor for the default help command.
cfg = configparser.ConfigParser()
cfg.read('matchacat/matchacat.ini')
#reddit = praw.Reddit(client_id = cfg.get('reddit', 'RedditClientID'), client_secret = cfg.get('reddit', 'RedditClientSecret'), username = cfg.get('reddit', 'RedditUsername'), password = cfg.get('reddit', 'RedditPassword'), useragent = 'matchacat v0.4 by Che5hire')
rcon = mcrcon.MCRcon()
#Client = discord.Client()
bot = commands.Bot(command_prefix = '$', description=abouttext)

#async def sec_clock():

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
		await bot.send_message(message.channel, '```css\n>shadman```')
			
	await bot.process_commands(message)
@bot.command(hidden=True)
async def mods(ctx):
	if ctx.message.author.id == 183304706624454656:
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
