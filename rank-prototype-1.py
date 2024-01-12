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

BOT_PREFIX = '!cr'
DB_FILE = "bot.db"

intents = discord.Intents.all() 
intents.reactions = True
intents.members = True

bot = commands.Bot(command_prefix=BOT_PREFIX, intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    
@bot.command()
async def addgame(ctx, *, name): 
    db = sqlite3.connect(DB_FILE)
    db.execute("INSERT OR IGNORE INTO games (name) VALUES (?)", (name,)) 
    await ctx.send(f"Added new game: {name}")
    
@bot.command()    
async def stats(ctx):
    db = sqlite3.connect(DB_FILE) 
    records = db.execute("""
        SELECT g.name, COALESCE(SUM(gt.end_time - gt.start_time), 0) AS playtime  
        FROM games g
        LEFT JOIN gametime gt ON gt.game_id = g.id AND gt.guild_id = ?
        GROUP BY g.id
    """, (ctx.guild.id,))
    
    message = f"**Stats for {ctx.guild.name}**\n"
    for row in records:
        game, playtime = row
        message += f"**{game}** - {int(playtime) // 60:,} minutes\n"
        
    await ctx.send(message)
    
@bot.command()
async def leaderboard(ctx, *, game):
    
    db = sqlite3.connect(DB_FILE)
    
    game_id = db.execute("SELECT id FROM games WHERE name = ?", (game,)).fetchone()[0]
    
    records = db.execute("""
        SELECT m.id, m.display_name, SUM(gt.end_time - gt.start_time) AS playtime
        FROM gametime gt 
        JOIN discord_members m on m.id = gt.member_id
        WHERE gt.guild_id = ? AND gt.game_id = ?  
        GROUP BY m.id
        ORDER BY playtime DESC, m.display_name
        LIMIT 10
    """, (ctx.guild.id, game_id))
    
    leaderboard = "**Leaderboard for {}**\n".format(game)
    for index, row in enumerate(records):
        id, name, playtime = row
        leaderboard += "{}. {} - {} minutes\n".format(index+1, name, round(playtime/60))
     
    await ctx.send(leaderboard)
    
# @bot.event    
# async def on_voice_state_update(member, before, after):
#     if after.channel:
#         # Joined a voice channel
#         game = discord.Game(name=member.activity.name) 
#         db = sqlite3.connect(DB_FILE)
#         cursor = db.cursor()
#         cursor.execute("SELECT id FROM games WHERE name = ?", (game.name,))
#         game_id = cursor.fetchone() 
#         if game_id is None:
#             cursor.execute("INSERT INTO games (name) VALUES (?)", (game.name,))
#             game_id = cursor.lastrowid
#         else : 
#             game_id = game_id[0]
        
#         cursor.execute("INSERT INTO gametime (guild_id, member_id, game_id, start_time) VALUES (?, ?, ?, ?)",
#                    (member.guild.id, member.id, game_id, datetime.now().timestamp()))
#         db.commit()
#         db.close()
        
#     if before.channel:
#         # Left voice channel 
#         db = sqlite3.connect(DB_FILE) 
#         db.execute("UPDATE gametime SET end_time = ? WHERE id = (SELECT id FROM gametime WHERE member_id = ? ORDER BY ID DESC LIMIT 1)",
#                    (datetime.now().timestamp(), member.id))
#         db.commit()
#         db.close()
@bot.event
async def on_presence_update(before,after):
    user = after
    
    if user.bot:
        return
    if user.voice and user.activity:
        print(f"{user} is playing {user.activity.name}")
        game = discord.Game(name=user.activity.name) 
        db = sqlite3.connect(DB_FILE)
        cursor = db.cursor()
        cursor.execute("SELECT id FROM games WHERE name = ?", (game.name,))
        game_id = cursor.fetchone() 
        if game_id is None:
            cursor.execute("INSERT INTO games (name) VALUES (?)", (game.name,))
            game_id = cursor.lastrowid
        else : 
            game_id = game_id[0]
        
        cursor.execute("INSERT INTO gametime (guild_id, member_id, game_id, start_time) VALUES (?, ?, ?, ?)",
                   (user.guild.id, user.id, game_id, datetime.now().timestamp()))
        db.commit()
        db.close()
    elif user.voice and not user.activity: # user is in a voice channel but not playing a game
        print(f"{user} is not playing a game")
        db = sqlite3.connect(DB_FILE) 
        db.execute("UPDATE gametime SET end_time = ? WHERE id = (SELECT id FROM gametime WHERE member_id = ? ORDER BY ID DESC LIMIT 1)",
                   (datetime.now().timestamp(), user.id))
        db.commit()
        db.close()
        
bot.run(TOKEN)