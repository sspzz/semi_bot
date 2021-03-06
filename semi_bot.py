import config
from semi import SuperFactory, SuperMeta
import json
import discord
from discord.ext import commands
import logging
import logging.config
from random import randrange
import random

# Utilities related to Discord
class DiscordUtils:
	@staticmethod
	async def embed(ctx, title, description, thumbnail=None, image=None):
		embed = discord.Embed(title=title, description=description)
		if thumbnail is not None:
			embed.set_thumbnail(url=thumbnail)
		if image is not None:
			embed.set_image(url=image)
		await ctx.send(embed=embed)

	@staticmethod
	async def embed_image(ctx, title, file, filename, description=None, footer=None, url=None):
		embed = discord.Embed(title=title)
		file = discord.File(file, filename=filename)
		embed.set_image(url="attachment://{}".format(filename))
		if description is not None:
			embed.description = description
		if footer is not None:
			embed.set_footer(text=footer)
		if url is not None:
			embed.url = url
		await ctx.send(file=file, embed=embed)

	@staticmethod
	async def embed_fields(ctx, title, fields, inline=True, thumbnail=None, url=None, image=None):
		file = None
		embed = discord.Embed(title=title)
		if thumbnail is not None:
			embed.set_thumbnail(url=thumbnail)
		for field in fields:
			embed.add_field(name=field[0], value=field[1], inline=inline)
		if url is not None:
			embed.url = url
		if image is not None:
			file = discord.File(image, filename="semi.png")
			embed.set_image(url="attachment://semi.png")
		await ctx.send(file=file, embed=embed)


#
# Setup
#
bot = commands.Bot(command_prefix="!")

logging.basicConfig(filename='semi_bot.log',
                    filemode='a',
                    format='[%(asctime)s] %(name)s - %(message)s',
                    datefmt='%d-%m-%Y @ %H:%M:%S',
                    level=logging.INFO)
logger = logging.getLogger('semi_bot')

def is_admin():
	def predicate(ctx):
		return ctx.message.author.id in config.discord_admins
	return commands.check(predicate)

def can_be_used_in(channel_id):
	def predicate(ctx):
		return ctx.message.channel.id == channel_id
	return commands.check(predicate)

#
# Commands
#
@bot.command(name="semi", aliases=["stats", "s"])
async def stats(ctx, token_id):
	logger.info("SEMI")
	try:
		semi = SuperFactory.get(token_id)
		traits = sorted(semi.meta.attributes, key=lambda t: t.trait_type)
		def field_from_trait(trait):
			return ("{} {}".format(trait.rarity_category, trait.trait_type.title()), "{} ({}%)".format(trait.value, round(trait.rarity*100, 2)))
		await DiscordUtils.embed_fields(ctx, semi.name, list(map(lambda t: field_from_trait(t), traits)), image=semi.pfp, url=semi.opensea_url)
	except:
		await ctx.send("Could not load SemiSuper {}".format(token_id))

@bot.command(name="pfp", aliases=["pic"])
async def pic(ctx, *args):
	logger.info("PFP")
	traits = None
	if len(args) == 0:
		token_id = random.randint(0, 5554)
	elif len(args) == 1:
		token_id = args[0]
	else:
		token_id = args[0]
		traits = args[1:]
	try:
		if traits is None:
			semi = SuperFactory.get(token_id)
			await DiscordUtils.embed_image(ctx, semi.name, semi.pfp, "semi.png", url=semi.opensea_url)
		else:
			semi, pfp = await SuperFactory.pfp_custom(token_id, traits)
			await DiscordUtils.embed_image(ctx, semi.name, pfp, "semi.png", url=semi.opensea_url)
	except:
		await ctx.send("Could not load SemiSuper {}".format(token_id))

@bot.command(name="tpfp", aliases=["tpic", "pfpnobg"])
async def pic_nobg(ctx, *args):
	logger.info("PFP NOBG")
	if len(args) == 0:
		token_id = random.randint(0, 5554)
	elif len(args) == 1:
		token_id = args[0]
	else:
		return
	try:
		semi = SuperFactory.get(token_id)
		await DiscordUtils.embed_image(ctx, semi.name, semi.pfp_nobg, "semi.png", url=semi.opensea_url)	
	except:
		await ctx.send("Could not load SemiSuper {}".format(token_id))

@bot.command(name="head")
async def pic(ctx, *args):
	logger.info("HEAD")
	if len(args) == 0:
		token_id = random.randint(0, 5554)
	elif len(args) == 1:
		token_id = args[0]
	else:
		return
	try:
		semi = SuperFactory.get(token_id)
		await DiscordUtils.embed_image(ctx, semi.name, semi.head, "semi.png", url=semi.opensea_url)	
	except:
		await ctx.send("Could not load SemiSuper {}".format(token_id))

@bot.command(name="thead", aliases=["headnobg"])
async def pic_nobg(ctx, *args):
	logger.info("HEAD NOBG")
	if len(args) == 0:
		token_id = random.randint(0, 5554)
	elif len(args) == 1:
		token_id = args[0]
	else:
		return
	try:
		semi = SuperFactory.get(token_id)
		await DiscordUtils.embed_image(ctx, semi.name, semi.head_nobg, "semi.png", url=semi.opensea_url)	
	except:
		await ctx.send("Could not load SemiSuper {}".format(token_id))

@bot.command(name="gm")
async def gm(ctx, *args):
	logger.info("GM")
	if len(args) == 0:
		token_id = random.randint(0, 5554)
	elif len(args) == 1:
		token_id = args[0]
	else:
		return
	try:
		semi = SuperFactory.get(token_id)
		await DiscordUtils.embed_image(ctx, semi.name, semi.gm, "semi.png", url=semi.opensea_url)	
	except:
		await ctx.send("Could not load SemiSuper {}".format(token_id))

@bot.command(name="gn")
async def gn(ctx, *args):
	logger.info("GN")
	if len(args) == 0:
		token_id = random.randint(0, 5554)
	elif len(args) == 1:
		token_id = args[0]
	else:
		return
	try:
		semi = SuperFactory.get(token_id)
		await DiscordUtils.embed_image(ctx, semi.name, semi.gn, "semi.png", url=semi.opensea_url)	
	except:
		await ctx.send("Could not load SemiSuper {}".format(token_id))

@bot.command(name="vs")
async def vs(ctx, *args):
	logger.info("VS")
	fight_round = None
	if len(args) == 0:
		token_id = random.randint(0, 5554)
		token_id2 = random.randint(0, 5554)
	elif len(args) == 1:
		token_id = args[0]
		token_id2 = random.randint(0, 5554)
	elif len(args) == 2:
		token_id = args[0]
		token_id2 = args[1]
	elif len(args) == 3:
		fight_round = args[0]
		token_id = args[1]
		token_id2 = args[2]
	else:
		return
	try:
		semi1, semi2, image = await SuperFactory.vs(token_id, token_id2, fight_round)
		await DiscordUtils.embed_image(ctx, "{} vs. {}".format(semi1.name, semi2.name), image, "semi.png")
	except Exception as e:
		logger.error(e.message)
		await ctx.send("Could not load SemiSuper {}".format(token_id))

@bot.command(name="vsg", aliases=["vsgif"])
async def gvs(ctx, *args):
	logger.info("VS GIF")
	try:
		gif = await SuperFactory.vs_gif(args[0] if len(args) > 0 else None)
		await DiscordUtils.embed_image(ctx, "Fight!", gif, "semi.gif")
	except:
		await ctx.send("Could not load SemiSuper {}".format(token_id))


@bot.command(name="say", aliases=["catchphrase", "phrase"])
async def catchphrase(ctx, *, msg):
	logger.info("CATCHPHRASE")
	try:
		words = msg.split()
		has_token_id = words[0].isnumeric()
		token_id = words[0] if has_token_id else random.randint(0, 5554)
		semi, image = await SuperFactory.catchphrase(token_id, " ".join(words[1 if has_token_id else 0:]))
		await DiscordUtils.embed_image(ctx, semi.name, image, "semi.png", url=semi.opensea_url)	
	except:
		await ctx.send("Could not load SemiSuper {}".format(token_id))

#
# Run bot
#
bot.run(config.discord_access_token)
