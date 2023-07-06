import os
from webserver import keep_alive

from datetime import datetime, timedelta, time
import asyncio
import discord
import pytz
from pytz import timezone

# Replace YOUR_TOKEN_HERE with your bot's token
TOKEN = os.environ['DISCORD_SECRET_TOKEN']
CHANNEL_ID = CHANNEL_ID_SECRET
SERVER_ID = SERVER_ID_SECRET

intents = discord.Intents.default()
intents.message_content = True
bot = discord.Client(intents=intents)
ist = timezone('Asia/Kolkata')

db = dict({})
message_time = '16:30'
count_response_time = ['17:30', '20:30']

st_time = [16, 30]
e_time = [20, 30]


# Data class
class UserWish:

	def __init__(self, b, l):
		self.b = b
		self.l = l

	def __str__(self):
		return f'b=> {self.b} : l=> {self.l}'


def canAccept(dt_string):
	if (dt_string is None): return False

	ist = pytz.timezone('Asia/Kolkata')
	dt_ist = dt_string.astimezone(ist)
	print(dt_ist)

	today = datetime.now(ist).date()

	start_time = time(st_time[0], st_time[1])
	end_time = time(e_time[0], e_time[1])

	start_datetime = ist.localize(datetime.combine(today, start_time))
	end_datetime = ist.localize(datetime.combine(today, end_time))
	print(start_datetime, end_datetime)

	return start_datetime <= dt_ist <= end_datetime


def addCount(msg, userId):
	dt_now = datetime.now(ist)
	if 'b' in msg:
		if userId not in db:
			uw = UserWish(None, None)
			db[userId] = uw
		db[userId].b = dt_now
	if (('l' in msg) and ('nill' not in msg)):
		if userId not in db:
			uw = UserWish(None, None)
			db[userId] = uw
		db[userId].l = dt_now
	print(db)


def getCount():
	bcount = 0
	lcount = 0

	for x in list(db.keys()):
		b = db[x].b
		l = db[x].l

		print(canAccept(b))

		if (b !=
		    None) and (datetime.now(ist) - b) < timedelta(hours=24) and canAccept(b):
			bcount += 1

		if (l !=
		    None) and (datetime.now(ist) - l) < timedelta(hours=24) and canAccept(l):
			lcount += 1

	reply = f'Breakfast : **{bcount}**\n\nLunch : **{lcount}**'

	return reply


async def getCountInfo():
	buser, luser = '', ''
	bcount, lcount = 0, 0

	for x in list(db.keys()):
		b, l = db[x].b, db[x].l

		user = await bot.fetch_user(x)
		if (b !=
		    None) and (datetime.now(ist) - b) < timedelta(hours=24) and canAccept(b):
			buser += f', {user.name}'
			bcount += 1

		if (l !=
		    None) and (datetime.now(ist) - l) < timedelta(hours=24) and canAccept(l):
			luser += f', {user.name}'
			lcount += 1

	buser = buser[2:]
	luser = luser[2:]

	reply = f'Breakfast : **{bcount}**\n\nLunch : **{lcount}**\n\n**Breakfast: ** {buser}\n\n**Lunch: ** {luser}'

	return reply


# Event handler for when the bot is ready
@bot.event
async def on_ready():
	print(f"Logged in as {bot.user}")
	asyncio.create_task(send_message_loop())
	asyncio.create_task(send_message_loop1())
	asyncio.create_task(send_message_loop2())


# Event handler for when the bot receives a message
@bot.event
async def on_message(message):
	if message.channel.id == CHANNEL_ID:
		if message.author == bot.user:
			return

		if message.content.startswith("-fc"):
			userId = message.author.id
			msg = message.content.lower()
			addCount(msg, userId)
			if (canAccept(datetime.now())):
				await message.add_reaction("\N{THUMBS UP SIGN}")

		if (message.content == '-count'):
			reply = getCount()
			await message.channel.send(reply)

		if (message.content.startswith('-count') and message.content.endswith('-i')):
			reply = await getCountInfo()
			await message.channel.send(reply)


async def send_message_loop():
	while True:
		print('...')
		now = datetime.now(ist).strftime("%H:%M")

		if now == message_time and datetime.now(ist).weekday() not in [4, 5]:
			print('ok')
			server = bot.get_guild(SERVER_ID)
			channel = server.get_channel(CHANNEL_ID)
			await channel.send(
			 '@everyone food count\n**-fc b** -> for breakfast\n**-fc l** -> for lunch\n**-fc bl** -> for breakfast and lunch'
			)

			await asyncio.sleep(24 * 60 * 60)

		else:
			print('.', now)
			await asyncio.sleep(60)


async def send_message_loop1():
	while True:
		print('...1')
		now = datetime.now(ist).strftime("%H:%M")

		if now == count_response_time[0] and datetime.now(ist).weekday() not in [
		  4, 5
		]:
			print('Count done')
			server = bot.get_guild(SERVER_ID)
			channel = server.get_channel(CHANNEL_ID)
			await channel.send(f'\nCount done\n\n{getCount()}')

			await asyncio.sleep(24 * 60 * 60)

		else:
			print('.', now)
			await asyncio.sleep(60)


async def send_message_loop2():
	while True:
		print('...2')
		now = datetime.now(ist).strftime("%H:%M")

		if now == count_response_time[1] and datetime.now(ist).weekday() not in [
		  4, 5
		]:
			print('Count done')
			server = bot.get_guild(SERVER_ID)
			channel = server.get_channel(CHANNEL_ID)
			await channel.send(f'\nCount done\n\n{getCount()}')

			await asyncio.sleep(24 * 60 * 60)

		else:
			print('.', now)
			await asyncio.sleep(60)


keep_alive()
bot.run(TOKEN)
