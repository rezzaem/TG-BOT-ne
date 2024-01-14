import discord
from discord.ext import commands
import sqlite3
from datetime import datetime, timedelta
from os import getenv
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the token from the .env file
TOKEN = getenv('token')

BOT_PREFIX = '!cr '
DB_FILE = "bot.db"

intents = discord.Intents.all() 
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")


