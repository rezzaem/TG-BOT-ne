import discord
from discord.ext import commands,tasks
import os
from dotenv import load_dotenv
import json
import random
# Load the .env file
load_dotenv()

# read auto react channels and reacts from json
with open('auto_react.json','r', encoding='utf-8') as f:
    data = json.load(f)


# Get the token from the .env file
TOKEN = os.getenv('token')


intents = discord.Intents.default() 
intents.reactions = True

bot = commands.Bot(command_prefix='MR ', intents=intents)

# load banner images 
banner_images = []
for image in os.listdir('banners'):
    if image.endswith('.png') or image.endswith('.jpg'):
        banner_images.append(image)
        
# Counter for looping through images
image_counter = 0

@tasks.loop(seconds=5)
async def change_banner():
    global image_counter
    guild = bot.get_guild(712292895515738134)
    if guild.premium_tier >= 2:
        banner = banner_images[image_counter]
        with open(f'banners/{banner}', 'rb') as f:
            await guild.edit(banner=f.read())
        
        # Increment the counter and reset if it exceeds the length of the images list
        image_counter = (image_counter + 1) % len(banner_images)

@bot.event
async def on_ready():
    change_banner.start()
    print(f'Logged in as {bot.user.name}')

try:
    @bot.event
    async def on_message(message):
        message.channel.id=str(message.channel.id) #make it string to can search and use in keys and json data
        if message.channel.id in data and not message.author.bot:

            await message.add_reaction(data[message.channel.id])  # Add the sticker reaction here

        await bot.process_commands(message)
except Exception as e:
    print(e)

@bot.command()
async def roleplay(ctx):
    # Your roleplay code here
    pass

@bot.command()
async def play(ctx):
    # Your music playback code here
    pass


bot.run(TOKEN)
