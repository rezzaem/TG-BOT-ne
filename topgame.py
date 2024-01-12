import discord
from discord.ext import commands, tasks 
import json


intents = discord.Intents.all() 
intents.reactions = True

bot = commands.Bot(command_prefix='MR', intents=intents)

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel and before.channel != after.channel: 
        # User joined voice 
        print(f"{member} joined {after.channel}")
    
    if before.channel and after.channel != before.channel:
        # User left voice
        print(f"{member} left {before.channel}")
    
    activity = member.activity
    if activity is not None:
        if activity.type == discord.ActivityType.playing: 
            game = activity.name
            print(f"{member} joined playing {game}")



bot.run('MTE5MTc1MTU5NjIyMTE1NzM5Nw.GR_Ovp.ZSMEWWf1HyoaxyB6x_UjIBBzqOj3pA8Y7mYIgI')

