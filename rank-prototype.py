import discord
from collections import defaultdict
from discord.ext import commands, tasks
import json
import asyncio

intents = discord.Intents.default() 
intents.reactions = True

bot = commands.Bot(command_prefix='MR', intents=intents)
# Dict to store voice state data
voice_states = {}

# Track game time totals
game_times = defaultdict(int) 

@bot.event
async def on_ready():
    update_leaderboard.start()

@tasks.loop(minutes=1)  
async def update_leaderboard():
    current_lb = {}
    
    # Build leaderboard dict
    for member_id, data in voice_states.items():
        member = bot.get_user(member_id)
        game = data["game"]
        time = data["time"]
        
        # Update total game time 
        game_times[game] += time
        
        if member.id not in current_lb:
            current_lb[member.id] = time
        else:
            current_lb[member.id] += time
            
    # Sort leaderboard        
    lb_sorted = sorted(current_lb.items(), 
                       key=lambda x: x[1], reverse=True)

    # Save leaderboard
    with open("leaderboard.txt", "w") as f: 
        f.write(json.dumps(lb_sorted)) 


@update_leaderboard.before_loop
async def before_print():
    await bot.wait_until_ready()
    


@bot.command()
async def leaderboard(ctx):
    with open("leaderboard.txt") as f:
        lb = json.load(f)
        
    embed = discord.Embed(title="Leaderboard")
    for i, (member_id, time) in enumerate(lb, start=1): 
        member = bot.get_user(int(member_id))
        embed.add_field(name=f"{i}. {member}", value=f"{time//60} hours")

    await ctx.send(embed=embed)
    
@bot.command()   
async def topgames(ctx):
    sorted_games = sorted(game_times.items(), 
                          key=lambda x: x[1], reverse=True)
                          
    embed = discord.Embed(title="Most Played Games")
    for i, (game, time) in enumerate(sorted_games[:5], start=1):
        embed.add_field(name=f"{i}. {game}", value=f"{time//60} hours") 
    
    await ctx.send(embed=embed)
    
# async def start_tasks():
#     await bot.wait_until_ready()  
#     update_leaderboard.start()

# bot.loop.create_task(start_tasks())
    


bot.run('MTE5MTc1MTU5NjIyMTE1NzM5Nw.GR_Ovp.ZSMEWWf1HyoaxyB6x_UjIBBzqOj3pA8Y7mYIgI')