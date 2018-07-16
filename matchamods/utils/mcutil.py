#This is a bunch of functions for administrating the minecraft server.
#By default the functions take the discord user as an argument.
try:	
	import discord, configparser, json, sys, mcrcon
	rcon = mcrcon.MCRcon()
	MCIP = ''
	MCPort =''
	MCPass = ''
	MCSupport = False
	RCONresult = ''
	with open('server.properties') as serpros: #Reads the server.properties file for the rcon info.
		for line in serpros.readlines():
			if line.startswith('server-ip='):
				MCIP = line[(line.find('=') + 1):].replace('\n', '') #Grabs the value after = and removes the newline characters at the end.
			if line.startswith('rcon.port='):
				MCPort = line[(line.find('=') + 1):].replace('\n', '')
				
			if line.startswith('rcon.password='):
				MCPass = line[(line.find('=') + 1):].replace('\n', '')
				
			if ((MCPass != '') and (MCPort != '') and (MCIP != '')):
				try:
					MCPort = int(MCPort)
					MCSupport = True
				except: #If this throws an exception (I'm expecting the int conversion to fail if you enter a non-numeric value into the field that determines the RCON port.) It won't enable RCON support even if the ini has the value set to true.
					print('Minecraft RCON details are incorrectly entered, check the server.properties file')
				break
		else:
			print('Minecraft RCON details are incorrectly entered, check the server.properties file')
	cfg = configparser.ConfigParser()
	cfg.read('matchacat/matchacat.ini')
	def rsearch(name):
		with open('whitelist.json', 'r') as f:
			whitelistJSON = json.load(f)
		with open('matchacat/matchacat.json', 'r') as f:
			matchacatJSON = json.load(f)
		MCuuid = ''
		'''finds a discord ID based off of minecraft username, returns None if nothing is found'''
		with open('whitelist.json', 'r') as f:
			whitelistJSON = json.load(f)
		for mc in whitelistJSON:
			print(mc)
			if mc['name'] == name:
				MCuuid = mc['uuid']
				break
		else:
			return None
		mcloop = 0
		for user in list(matchacatJSON['users'].items()):
			print(str(user))
			if user[1]['MCuuid'] == MCuuid:
				return user[0]
		else:
			return None
	def search(member):
		'''finds a minecraft username based off of discord ID, returns None if nothing is found'''
		discordID = str(member.id)
		with open('whitelist.json', 'r') as f:
			whitelistJSON = json.load(f)
		with open('matchacat/matchacat.json', 'r') as f:
			matchacatJSON = json.load(f)
		if matchacatJSON['users'].get(discordID, None) != None:
			if matchacatJSON['users'][discordID].get('MCuuid', None) != None:
				for mc in whitelistJSON:
					if mc['uuid'] == matchacatJSON['users'][discordID]['MCuuid']:
						return mc['name']
				else:
					return None
			else:
				return None
		else:
			return None 
	def whitelist(member, MCuser):
		'''Whitelists a user, takes a server member as member and a string reprisenting the member's minecraft username.
		Will return True if it successfully whitelists the user.'''
		discordID = str(member.id)
		RCONresult = ''
		MCuuid = ''
		MCblacklist = '' #If the user is already whitelisted it will remove them and then add the new MCuser
		with open('matchacat/matchacat.json') as f:
			matchacatJSON = json.load(f)
			MCuuid = matchacatJSON['users'][str(member.id)].get('MCuuid', '')
		with open('whitelist.json') as f:
			whitelistJSON = json.load(f)
			for mc in whitelistJSON:
				if mc['uuid'] == MCuuid:
					MCblacklist = mc['name']
		if MCblacklist != '':
			try:
				rcon.connect(MCIP, MCPort, MCPass)
				rconcommand = 'whitelist remove {}'.format(MCblacklist)
				RCONresult = rcon.command(rconcommand)
				rcon.disconnect()
			except:
				print('failed to blacklist')
				e = sys.exc_info()[0]
				print(e)
				return False
		if RCONresult.startswith('Could '):
			return False
		try:
			rcon.connect(MCIP, MCPort, MCPass)
			rconcommand = 'whitelist add {}'.format(MCuser)
			RCONresult = rcon.command(rconcommand)
			rcon.disconnect()
		except:
			print('failed to whitelist')
			e = sys.exc_info()
			print(e)
			return False
		if RCONresult.startswith('Could '):
			print('no server')
			return False
		with open('whitelist.json') as f:
			whitelistJSON = json.load(f)
			for mc in whitelistJSON:
				if mc['name'] == MCuser:
					MCuuid = mc['uuid']
		try:	
			if matchacatJSON['users'].get(discordID, None) != None:
				matchacatJSON['users'][discordID]['MCuuid'] = MCuuid
			else:
				matchacatJSON['users'].update({discordID : {'MCuuid' : MCuuid}})
			with open('matchacat/matchacat.json', 'w') as f:
				f.write(json.dumps(matchacatJSON, sort_keys=True, indent=2, separators=(',', ': ')))
		except:
			e = sys.exc_info()
			print(e)
			return False
		return True
			
	def blacklist(user):
		'''Removes a user from the whitelist, takes a guild member'''
		MCuser = ''
		MCuuid = ''
		discordID = str(user.id)
		with open('matchacat/matchacat.json') as f:
			matchacatJSON = json.load(f)
		MCuuid = matchacatJSON['users'][discordID]['MCuuid']
		with open('whitelist.json') as f:
			whitelistJSON = json.load(f)
			for mc in whitelistJSON:
				if mc['uuid'] == MCuuid:
					MCuser = mc['name']
					return
				else:
					return False
		try:
			rcon.connect(MCIP, MCPort, MCPass)
			rconcommand = 'whitelist remove {}'.format(MCblacklist)
			RCONresult = rcon.command(rconcommand)
			rcon.disconnect()
		except:
			return False
		matchacat
		with open('matchacat/matchacat.json', 'w') as f:
			f.write(json.dumps(matchacatJSON, sort_keys=True, indent=2, separators=(',', ': ')))
			
	def ban(user):
		'''Bans a user, takes a guild member as an argument'''
		with open('whitelist.json', 'r') as f:
			whitelistJSON = json.load(f)
		with open('matchacat/matchacat.json', 'r'):
			matchacatJSON = json.load(f)
	def unban(user):
		'''Unbans a user, takes a guild member as an argument'''
except:
	e = sys.exc_info()
	print(e)
