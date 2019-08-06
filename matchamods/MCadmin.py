#Commands for staff only
import json, configparser, discord
from discord.ext import commands	
cfg = configparser.ConfigParser()
cfg.read('matchacat/matchacat.ini')
staffroleID = cfg.get('bot', 'StaffID')
class Admin(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
	@commands.command(description='Adds a tag for people to use.', hidden=True)
	async def addtag(self, ctx, tagname=None, *tagtext):
		try:
			if discord.utils.get(ctx.message.author.roles, id=int(staffroleID)) != None:
				#Tags are short messages that can be pasted into chat by matchacat, things like tutorials, FAQs and copypastas. Saved in a seprate section (tags) under matchacat.json.
				if tagname == None:
					await ctx.send("Usage: `$addtag` `tagname` `tagtext`") 
				elif len(tagtext) == 0:
					await ctx.send("You can't add a tag with no text.")
				else:	
					tagtext = ' '.join(tagtext)
					matchacatJSON = json.load(open('matchacat/matchacat.json', 'r'))
					matchacatJSON['tags'].update({tagname : tagtext})
					open('matchacat/matchacat.json', 'w').write(json.dumps(matchacatJSON, sort_keys=True, indent=2, separators=(',', ': ')))
					await ctx.send('Successfully added a tag named `' + tagname + '` with the text: ' + tagtext)
		except:
			e = sys.exc_info()[0]
			print(e)
	@commands.command(hidden=True)
	async def deltag(self, ctx, tagname):
		try:
			if discord.utils.get(ctx.message.author.roles, id=int(staffroleID)) != None:
				matchacatJSON = json.load(open('matchacat/matchacat.json', 'r'))
				matchacatJSON['tags'].pop(tagname)
				open('matchacat/matchacat.json', 'w').write(json.dumps(matchacatJSON, sort_keys=True, indent=2, separators=(',', ': ')))
				await ctx.send('Removed.')
		except:
			e = sys.exc_info()[0]
			print(e)
def setup(bot):
	bot.add_cog(Admin(bot))
