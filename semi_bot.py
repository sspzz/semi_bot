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
	async def embed(ctx, title, description, thumbnail=None, image=None, color=discord.Embed.Empty):
		file = None
		embed = discord.Embed(title=title, description=description, color=color)
		if thumbnail is not None:
			file = discord.File(thumbnail, filename="semi.png")
			embed.set_thumbnail(url="attachment://semi.png")
		if image is not None:
			file = discord.File(image, filename="semi.png")
			embed.set_image(url="attachment://semi.png")
		await ctx.send(file=file, embed=embed)

	@staticmethod
	async def embed_image(ctx, title, file, filename, description=None, footer=None, url=None, color=discord.Embed.Empty):
		embed = discord.Embed(title=title, color=color)
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
	async def embed_fields(ctx, title, fields, description=None, inline=True, thumbnail=None, url=None, image=None, color=discord.Embed.Empty):
		file = None
		embed = discord.Embed(title=title, color=color)
		if thumbnail is not None:
			file = discord.File(thumbnail, filename="semi.png")
			embed.set_thumbnail(url="attachment://semi.png")
		for field in fields:
			embed.add_field(name=field[0], value=field[1], inline=inline)
		if url is not None:
			embed.url = url
		if image is not None:
			file = discord.File(image, filename="semi.png")
			embed.set_image(url="attachment://semi.png")
		if description is not None:
			embed.description = description
		await ctx.send(file=file, embed=embed)

	@staticmethod
	def bg_color(semi):
		bg = semi.meta_trait("background").lower()
		try:
			if "purple" in bg:
				if semi.is_villain:
					return discord.Colour.dark_purple()
				else:
					return discord.Colour.purple()
			elif "pink" in bg:
				if semi.is_villain:
					return discord.Colour.dark_purple()
				else:
					return discord.Colour.purple()
			elif "magenta" in bg:
				if semi.is_villain:
					return discord.Colour.dark_magenta()
				else:
					return discord.Colour.magenta()
			elif "red" in bg:
				if semi.is_villain:
					return discord.Colour.dark_red()
				else:
					return discord.Colour.red()
			elif "teal" in bg:
				if semi.is_villain:
					return discord.Colour.dark_teal()
				else:
					return discord.Colour.teal()
			elif "blue" in bg:
				if semi.is_villain:
					return discord.Colour.dark_blue()
				else:
					return discord.Colour.blue()
			elif "orange" in bg:
				if semi.is_villain:
					return discord.Colour.dark_orange()
				else:
					return discord.Colour.orange()
			elif "yellow" in bg:
				if semi.is_villain:
					return discord.Colour.dark_orange()
				else:
					return discord.Colour.orange()
			elif "light gray" in bg:
				return discord.Colour.light_grey()
			elif "dark gray" in bg:
				return discord.Colour.dark_grey()
		except:
			return discord.Colour.light_grey()



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


def can_be_used_in(channel_id):
	def predicate(ctx):
		return ctx.message.channel.id == channel_id
	return commands.check(predicate)

def has_role(role_id):
	def predicate(ctx):
		return discord.utils.find(lambda r: r.id == role_id, ctx.message.guild.roles) in ctx.message.author.roles
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
		await DiscordUtils.embed_fields(ctx, semi.name, list(map(lambda t: field_from_trait(t), traits)), thumbnail=semi.pfp, url=semi.opensea_url)
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
# Fight Night
#

@has_role(930936361744212030)
@can_be_used_in(961901966630457384)
@bot.command(name="multi")
async def fight(ctx, *args):
	if len(args) == 0:
		token_id = random.randint(0, 5554)
		token_id2 = random.randint(0, 5554)
	elif len(args) == 1:
		token_id = args[0]
		token_id2 = random.randint(0, 5554)
	elif len(args) >= 2:
		token_id = args[0]
		token_id2 = args[1]	
	semi1, semi2, image = await SuperFactory.vs(token_id, token_id2)
	multi = int(args[2]) if len(args) >= 3 else 15
	await DiscordUtils.embed_fields(ctx, "Damage multiplier (traits cap at {})".format(multi), [(semi1.name, "{}".format(semi1.damage_multiplier(traits_cap=multi))), (semi2.name, "{}".format(semi2.damage_multiplier(traits_cap=multi)))], image=image)

import asyncio 

@has_role(930936361744212030)
@can_be_used_in(961901966630457384)
@bot.command(name="fight")
async def fight(ctx, token_id, token_id2):
	logger.info("FIGHT")

	class Player(object):
		def __init__(self, semi):
			self.semi = semi
			self.health = 50
			self.multiplier = semi.damage_multiplier()

	semi1, semi2, image_vs = await SuperFactory.vs(token_id, token_id2)#, fight_round)
	player1 = Player(semi1)
	player2 = Player(semi2)
	round_number = 1

	# Display fight start	
	title = "{} vs. {}".format(semi1.name, semi2.name)
	desc = "The contestants are nearly ready, and the battle is about to begin!"
	await DiscordUtils.embed_image(ctx, title, image_vs, "semi.png", description=desc, color=discord.Color.red())

	# await asyncio.sleep(5)

	# Game rounds loop
	while True:
		# Coin toss on who goes first this round
		p1_first = random.SystemRandom().randint(0, 1) == 1
		round_order = [player1, player2] if p1_first else [player2, player1]

		# Display round start
		title = "ROUND {}, FIGHT!".format(round_number)
		desc = "The round is about to begin!\n\nAfter a coin toss **{} gets first strike**!".format(round_order[0].semi.name)
		await DiscordUtils.embed(ctx, title, desc, color=discord.Color.red(), thumbnail="resources/assets/fight.png")

		# await asyncio.sleep(5)

		# Performs attack, returns True if attack leads to game over
		async def attack(attacker, defender) -> bool:
			# Roll dice and deal damage based on multiplier
			roll = random.SystemRandom().randint(1, 6)
			damage = round(attacker.multiplier * roll, 3)
			defender.health = round(defender.health - damage, 3)
			game_over = defender.health <= 0

			# Display attack
			title = "{} attacks!".format(attacker.semi.name)
			fight_moves = [
				"performs semi-savage kung-fu",
				"exhibits decent boxing skills",
				"lands a moderately powerful punch",
				"does some ferocious tickling"
			]
			desc = "{} **rolls a {}** and {}, **doing {} damage**!".format(attacker.semi.name, roll, random.choice(fight_moves), damage)
			fields = [("Roll", "{}".format(roll)), ("Multiplier", "{}x".format(attacker.multiplier)), ("Damage", "{}".format(damage))]
			color = DiscordUtils.bg_color(attacker.semi)
			await DiscordUtils.embed_fields(ctx, title, fields, description=desc, thumbnail=attacker.semi.pfp_small, color=color)

			# await asyncio.sleep(3)

			# Display winner if game over
			if game_over:
				rounds_desc = [
					"semi-gruelling and mildy verocious",
					"somewhat engaging and exciting",
					"mostly cute and partly entertaining",
					"moderately vicious and possibly funny"
				]
				desc = "After {} {} rounds, **{} WINS** with {} health remaining!\n\nCONGRATULATIONS!".format(round_number, random.choice(rounds_desc), attacker.semi.name, attacker.health)
				await DiscordUtils.embed(ctx, 
										"FIGHT OVER!",
										desc,
										image=attacker.semi.pfp,
										color=discord.Colour.red())
			return game_over
		
		game_over = await attack(round_order[0], round_order[1])
		if not game_over:
			# await asyncio.sleep(5)
			game_over = await attack(round_order[1], round_order[0])		
		if game_over:
			break
		else:
			# Display round summary
			await DiscordUtils.embed_fields(ctx, 
											"ROUND {} OVER!".format(round_number), 
											list(map(lambda p: (p.semi.name, "{} health remaining".format(p.health)), round_order)),
											description="The round is over, both fighters are still in the game!",
											color=discord.Color.red())
			round_number += 1

#
# Run bot
#
bot.run(config.discord_access_token)
