#Commands for the matchmaking channel.
import random, json, sys, discord, configparser
from steam import SteamID
from discord.ext import commands

cfg = configparser.ConfigParser()
cfg.read('matchacat/matchacat.ini')

if cfg.getboolean("minecraft", "WhiteList"):
	from matchamods.utils import mcutil

class Gaming(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		self.services = ['steam', 'minecraft', 'showdown']#the services our bot supports.
	@commands.command(description='Adds a username so people can easily see it.', pass_context=True)
	async def adduser(self, ctx, service=None, username=None):
		discordID = str(ctx.message.author.id)
		if (service == None) or (not service in self.services):
			await ctx.send(', '.join(self.services))
			await ctx.send("If you are confused about how to use a service with commands type `$service service`")
		elif(username==None):
			await ctx.send('You need to enter something for a username.')
		elif(service == self.services[0]):#steam
			#we need to figure out if the 'username' variable is a steamID, steamID64 or a profileurl.
			if username.startswith('steamcommunity.com/'):
				username = 'http://' + username
				username = SteamID.from_url(username).id
			elif (username.startswith('https://steamcommunity.com/')) or (username.startswith('http://steamcommunity.com/')):
				try:
					username = SteamID.from_url(username).id
				except:
					e = sys.exc_info()[0]
					print(e)
					await ctx.send(username)
			try:
				int(username)#this will throw an exception if username is not a number and therefore not a steamID
				username = SteamID(username).as_64#We want a steam64 ID, this will make sure we have that. 
			except:
				await ctx.send(username + ' is not a steamID or steam profile URL')
			else:
				try:
					matchacatJSON = json.load(open('matchacat/matchacat.json', 'r'))
					#matchacatJSON['services']['steam'].update({str(username) : str(discordID)})#Makes reverse searching easier.
					if matchacatJSON['users'].get(discordID, None) == None:
						matchacatJSON['users'].update({discordID :{'steamID' : username}})
					else: 
						matchacatJSON['users'][discordID]['steamID'] = str(username)
					open("matchacat/matchacat.json", "r+").write(json.dumps(matchacatJSON, sort_keys=True, indent=2, separators=(',', ': ')))
				except:
					await ctx.send('There was an error reading/writing to the JSON')
					e = sys.exc_info()
					print(e)
				else:
					await ctx.send('Successfully added')
		elif (service == self.services[1]) and cfg.getboolean("minecraft", "WhiteList"): #minecraft
			if mcutil.whitelist(ctx.message.author, username):#This whitelists the user to our minecraft server
				await ctx.send('You were whitelisted to our server.')
			else:
				await ctx.send('There was an error and we could not whitelist you, make sure you entered your username correctly then try again or contact an admin for assistance.')
		elif service == self.services[2]:#Pokemon Showdown
			with open('matchacat/matchacat.json', 'r+') as f:
				matchacatJSON = json.load(f)
				PSuser =username.lower().replace(" ", "")#Little known fact, you can enter spaces into an argument by wrapping it with quotes, we don't want that.
				if matchacatJSON['users'].get(discordID, None) != None:
					matchacatJSON['users'][discordID]['PSuser'] = PSuser
				else:
					matchacatJSON['users'].update({discordID : {'PSuser' : PSuser}})
			with open('matchacat/matchacat.json', 'w') as f:
				f.write(json.dumps(matchacatJSON, sort_keys=True, indent=2, separators=(',', ': ')))
				await ctx.send('Added')
			
	@commands.command(description='Gives instructions on how to use a service and what the service is.')
	async def service(self, ctx, service=None):
		if (service == None) or (not service in self.services):
			await ctx.send("Usage $service service\nAvailible services: " + ', '.join(self.services))
		elif service == self.services[0]:#Steam
			await ctx.send("This is your steam account. Due to the freedom you're given with nicknames you will need to enter the url to your steam account or steamID in place of a username when using `$adduser`")
		elif (service == self.services[1]) and not cfg.getboolean("minecraft", "WhiteList"):#If Minecraft support is disabled.
			await ctx.send("Minecraft support is disabled.")
		elif service == self.services[1]:#Minecraft
			await ctx.send("Adding your Minecraft username will automatically add you to our Minecraft server's whitelist.")
	@commands.command(description="Tells you the user's other usernames. The reverse of `whois`", pass_context=True, aliases=['othernames','aliases','usernames'])
	async def names(self, ctx, member: discord.Member=None, service=None):
		if member == None:
			member = ctx.message.author
		discordID = str(member.id)
		with open('matchacat/matchacat.json', 'r') as f:
			matchacatJSON = json.load(f)
		if matchacatJSON['users'].get(discordID, None) != None:
			if service == None:
				UserList = []
				if matchacatJSON['users'][discordID].get('steamID') != None:
					UserList += ['Steam: ' + (SteamID(matchacatJSON['users'][discordID]['steamID']).community_url)]
				if matchacatJSON['users'][discordID].get('MCuuid') != None:
					print(matchacatJSON['users'][discordID].get('MCuuid'))
					MCuser = mcutil.search(member)
					print(MCuser)
					if MCuser != None:
						UserList += ['Minecraft: ' + MCuser]
				if matchacatJSON['users'][discordID].get('PSuser') != None:
					UserList += ['Showdown: ' + matchacatJSON['users'][discordID].get('PSuser')]
				if UserList != []:
					await ctx.send('\n'.join(UserList))
				else:
					await ctx.send('This user has no names registered.')
			if service == self.services[0]:#Steam
				if matchacatJSON['users'][discordID].get('steamID', None) != None:
					steamurl = SteamID(matchacatJSON['users'][discordID]['steamID']).community_url
					await ctx.send(steamurl)
			if service == self.services[1]:#Minecraft
				MCuser = mcutil.search(member)
				if MCuser == None:
					await ctx.send('Could not find username.')
				else:
					await ctx.send('{}'.format(MCuser))
			if service == self.services[2]:#Showdown
				showdown = matchacatJSON['users'][discordID].get('PSuser')
				if showdown != None:
					ctx.send(showdown)
				else:
					ctx.send('This user has no pokemon showdown nickname.')
		else:
			await ctx.send('This user has no usernames registered')
	@commands.command(description="Tells you what Discord user owns a username on another service. The reverse of `names`", aliases=['discordname'])
	async def whois(self, ctx, service=None, username=None):
		if service == None:
			await ctx.send('Usage `$whois service username`\nCheck $services for more info')
		else:
			try:
				with open('matchacat/matchacat.json', 'r') as f:
					matchacatJSON = json.load(f)
			except:
				await ctx.send('There was an error reading/writing to the JSON')
				e = sys.exc_info()
				print(e)
			if service == self.services[2]:#Showdown
				username = username.lower()
				for user in matchacatJSON['users'].items():
					print(user)
					if user[1].get('PSuser') == username:
						await ctx.send('<@{}>'.format(user[0]))
						break
				else:
					await ctx.send('No Discord user found.')
			elif (service == self.services[1]) and cfg.getboolean("minecraft", "WhiteList"):#Minecraft
				discordID = mcutil.rsearch(username)
				if discordID != None:
					await ctx.send('<@{}>'.format(discordID))
				else:
					await ctx.send('Could not find a user by that name.')
			elif service == self.services[0]:#steam
				print(username)
				username = str(SteamID.from_url(username).as_64)
				print(username)
				for user in matchacatJSON['users'].items():
					print(user)
					if user[1].get('steamID') == username:
						await ctx.send('<@{}>'.format(user[0]))
						break
				else:
					await ctx.send('No Discord user found.')
def setup(bot):
	bot.add_cog(Gaming(bot))
