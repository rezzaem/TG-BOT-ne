import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import json

# Load the .env file
load_dotenv()

# read auto react channels and reacts from json
with open('auto_react.json','r', encoding='utf-8') as f:
    data = json.load(f)


# Get the token from the .env file
TOKEN = os.getenv('token')

intents = discord.Intents.default()
intents.reactions = True

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')

@bot.event
async def on_message(message):
    message.channel.id=str(message.channel.id) #make it string to can search and use in keys and json data
    if message.channel.id in data and not message.author.bot:

        await message.add_reaction(data[message.channel.id])  # Add the sticker reaction here

    await bot.process_commands(message)

@bot.command()
async def roleplay(ctx):
    # Your roleplay code here
    pass

@bot.command()
async def play(ctx):
    # Your music playback code here
    pass

bot.run(TOKEN)
