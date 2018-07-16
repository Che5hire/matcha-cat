#pokemon related commands like $sprite
import random, json, requests, discord, pandas
from discord.ext import commands	
#print('WCfun loaded')
class Pokemon():
	def __init__(self, bot):
		self.bot = bot		
	@commands.command(description="Displays a shiny pokemon sprite.")
	async def sprite(self, ctx, *pokemon):
		if (len(pokemon) == 0):
			await ctx.send('You need to enter the name of a pokemon')
		else:
			spritestring = " ".join(pokemon).lower()
			if((spritestring.startswith('mega ')) or (spritestring.endswith(' mega'))):
				print(spritestring)
				spritestring = spritestring.replace('mega ', '')
				spritestring = spritestring.replace(' mega', '')
				spritestring = (spritestring + '-mega')
				if (spritestring.find(' x-') != -1):
					spritestring = spritestring.replace(' x', '')
					spritestring = (spritestring + 'x')
				if (spritestring.find(' y-') != -1):
					spritestring = spritestring.replace(' y', '')
					spritestring = (spritestring + 'y')
			if (spritestring.startswith('alola ') or spritestring.startswith('alolan ')) or (spritestring.endswith(' alola') or spritestring.endswith(' alolan')):
				if spritestring.startswith('alola '):
					spritestring = spritestring.replace('alola ', '')
				elif spritestring.startswith('alolan '):
					spritestring = spritestring.replace('alolan ', '')
				elif spritestring.endswith(' alola'):
					spritestring = spritestring.replace(' alola', '')
				elif spritestring.endswith(' alolan'):
					spritestring = spritestring.replace(' alolan', '')
				spritestring += '-alola'
			if(spritestring.startswith('tapu ')):
				spritestring = spritestring.lower().replace(" ", "")
			if((spritestring.endswith(' male')) and (spritestring.find('nidoran') != -1)):
				spritestring = spritestring.lower().replace(" male", "_m")
			elif((spritestring.endswith(' female')) and (spritestring.find('nidoran') != -1)):
				spritestring = spritestring.lower().replace(" female", "_f")
			oolist = ['jangmo-o', 'hakamo-o', 'kommo-o']
			if(spritestring in oolist):
				spritestring = spritestring.lower().replace("-", "")
			spritestring = spritestring.lower().replace(" ", "-")
			spritestring = "http://play.pokemonshowdown.com/sprites/xyani-shiny/{}.gif".format(spritestring)
			if (requests.head(spritestring).headers.get('content-type').startswith('image') == True):#This really funky if statement basically checks if the URL is a link to an image file. If it 404s it will return False. The full string that returns when it runs the .startswith() should be image/gif but I made it look for 'image' just in case other formats are used.
				await ctx.send(spritestring)
			else:
				await ctx.send('Could not find the sprite you are looking for.')
	@commands.command(description="Displays the user's showdown ladder.", pass_context=True)
	async def ladder(self, ctx, member : discord.Member=None, tier=None):
		if member == None:
			member = ctx.message.author
		with open('matchacat/matchacat.json', 'r') as f:
			matchacatJSON = json.load(f)
		if matchacatJSON['users'].get(str(member.id), None) != None:
			if matchacatJSON['users'][str(member.id)].get('PSuser', None) != None:
				PSuser = matchacatJSON['users'][str(member.id)]['PSuser']
				url = 'https://pokemonshowdown.com/users/' + PSuser
				html = requests.get(url).content
				df_list = pandas.read_html(html)
				df = df_list[-1]
				laddertitle = ''
				if PSuser == member.name.lower():
					laddertitle = 'Ladder statistics for {}'.format(member.name)
				else:
					laddertitle = 'Ladder statistics for {} ({})'.format(member.name, PSuser)
				embed = discord.Embed(
					colour = discord.Colour.red(),
				)
				embed.set_author(name=laddertitle, icon_url=member.avatar_url)
				print(member.avatar_url)
				laddername = []
				ladderElo = []
				ladderGXE = []
				ladderGlicko = []
				for Name in df[0]:
					Name = str(Name)
					if Name.find(' ladder') == (-1):
						laddername += [Name]
				for Elo in df[1]:
					Elo = str(Elo)
					if Elo.find('Elo') == (-1):
						ladderElo += [Elo]
				for GXE in df[2]:
					GXE = str(GXE)
					if GXE.find('(more games needed)') != -1:
						ladderGXE += ['N/A']
					elif GXE.find('GXE') == (-1):
						ladderGXE += [GXE]
				for Glicko in df[3]:
					Glicko = str(Glicko)
					if Glicko.find('Glicko') == (-1):
						if Glicko.find('nan') != (-1):
							ladderGlicko += ['N/A']
						else:
							ladderGlicko += [Glicko]
				if tier != None:
					try:
						ladderno = laddername.index(tier)
						embed.add_field(name='Ladder', value=(laddername[ladderno]), inline=True)
						embed.add_field(name='Elo', value=(ladderElo[ladderno]), inline=True)
						embed.add_field(name='GXE / Glicko', value=(' / '.join([ladderGXE[ladderno], ladderGlicko[ladderno]])), inline=True)
					except:
						await ctx.send(url + '\nTier not found.')
						return
				else:
					for Name, Elo, GXE, Glicko in zip(laddername, ladderElo, ladderGXE, ladderGlicko):
						Elo = 'Elo: ' + Elo
						GXE = 'GXE: ' + GXE
						Glicko = 'Glicko-1: ' + Glicko
						embed.add_field(name=Name, value=('\n'.join([Elo, GXE, Glicko])), inline=True)
				await ctx.send(url, embed=embed)

			else:
				await ctx.send('That user does not have a showdown nickname registered')
		else:
			await ctx.send('That user does not have a showdown nickname registered')
def setup(bot):
	bot.add_cog(Pokemon(bot))
