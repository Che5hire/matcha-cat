#commands for just for fun.	
import random, json, discord, urllib.request, configparser
from discord.ext import commands
cfg = configparser.ConfigParser()
cfg.read('matchacat/matchacat.ini')
class Fun():
	def __init__(self, bot):
		self.bot = bot
	#Commands for tags which are 
	@commands.command(description='Makes this bot post the text in a tag.')
	async def tag(self, ctx, tag=None):
		matchacatJSON = json.load(open('matchacat/matchacat.json', 'r+'))
		if tag == None:
			await ctx.send('Usage `$tag tag`')
			await ctx.send('Avalible tags:\n' + '`' + ', '.join(matchacatJSON['tags'].keys()) + '`')
		else:
			tag = matchacatJSON['tags'].get(tag, 'There is no tag with that name.\nAvalible tags:\n' + '`' + ', '.join(matchacatJSON['tags'].keys()) + '`')
			#turns the tag varible into the text the tag is supposed to print.
			await ctx.send(tag)
	@commands.command(aliases=['color'], description='Colours your name.')
	async def colour(self, ctx, namecolour = None):
		if(namecolour == None):
			colourroles = []
			for role in ctx.message.guild.roles:
				if role.name.startswith('[Colour]'):
					colourroles += [role.name[8:]]
					
			await ctx.send('Usage: `$colour colour`\nAvailible colours: `' + ', '.join(colourroles) + '`')
		else:
			colour = ('[Colour]' + namecolour)
			removeroles = []
			for r in ctx.message.author.roles:
				#removing every role that starts with [Colour]
				if r.name.startswith('[Colour]'):
					try:
						await ctx.message.author.remove_roles(r)
					except:
						e = sys.exc_info()[0]
						print(e)
			
			rolecolour = discord.utils.get(ctx.message.guild.roles, name=colour)
			try:
				await ctx.message.author.add_roles(rolecolour)
			except:
				e = sys.exc_info()[0]
				print(e)
	@commands.command(description="Gives a random image based on the tags you enter. Typing 'top:' etc will give you the result that's the highest for that quality (example: 'top:score' gives you the highest scoring post). Putting a '~' behind a tag will make Matcha Cat randomly pick between those tags. This command can only be used in NSFW channels.")
	async def gelbooru(self, ctx,*tags):
		if ctx.message.channel.is_nsfw():
			tags = list(tags)
			imglimit = '100'#How many images will be pulled up, 100 is the max Gelbooru allows.
			ortags = []
			for tag in tags:
				if tag.startswith('~'):
					ortags += [tag]
				elif tag.find('top:') != -1:
					tags[tags.index(tag)] = tag.replace('top:', 'sort:')
					imglimit = '1'#This makes sure the top result is always picked it's also pointless to pull more if the top is what we want.
			else:
				if len(ortags) != 0:
					for tag in ortags:
						tags.remove(tag)
					tags += [random.choice(ortags).replace('~', '')]
			tags = ' '.join(tags)
			tags += ' ' + cfg.get('booru', 'Tags')
			urlinput = 'https://gelbooru.com/index.php?page=dapi&s=post&q=index&json=1&limit={}&tags={}'.format(imglimit, tags)
			webURL = urllib.request.urlopen(urlinput)
			data = webURL.read()
			#imgJSON = json.loads(data.decode(encoding))
			try:
				img = random.choice(json.loads(data.decode("utf-8")))
			except json.decoder.JSONDecodeError:
				await ctx.send('Could not find any images with the tags: `' + tags +'`')
			else:
				embed = discord.Embed(colour=discord.Colour.blue())
				embed.add_field(name='Score', value=img['score'], inline=True)
				imgrating = ''
				if img['rating'] == 's':
					imgrating = 'Safe🍬'
				if img['rating'] == 'q':
					imgrating = 'Questionable🌶'
				if img['rating'] == 'e':
					imgrating = 'Explicit🔥'
				embed.add_field(name='Rating', value=imgrating, inline=True)
				if not img['file_url'].endswith('.webm'):
					embed.set_image(url=img['file_url'])
				embed.set_image(url=img['file_url'])
				embed.set_author(name='ID: {}'.format(img['id']), icon_url='https://gelbooru.com/favicon.png', url='https://gelbooru.com/index.php?page=post&s=view&id={}'.format(img['id']))
				if img['file_url'].endswith('.webm'):
					await ctx.send(embed=embed)
					await ctx.send(img['file_url']) 
				else:
					embed.set_image(url=img['file_url'])
					await ctx.send(embed=embed)
		else: 
			await ctx.send('This command cannot be used in SFW channels.')
	@commands.command(aliases = ['role','iam'])
	async def togglerole(self, ctx, role=None):
		if role == None:
			ctx.send('Usage: `$togglerole role`')
		else:
			role = role.lower()
			role = '[' + role + ']'
			role = discord.utils.get(ctx.message.guild.roles, name=role)
			if role in ctx.message.author.roles:
				await ctx.message.author.remove_roles(role)
				await ctx.send('You have been removed from the {} role.'.format(role))
			else:
				try:
					await ctx.message.author.add_roles(role)
				except:
					await ctx.send('The role you have entered does not exist.')
				else:
					await ctx.send('You have been added to the {} role.'.format(role))
def setup(bot):
	bot.add_cog(Fun(bot))
