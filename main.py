import discord
from discord.ext import commands, tasks
import os
import youtube_dl
import asyncio

token = "set ur token here"



intents = discord.Intents.default()
intents.typing = False
intents.presences = False
intents.voice_states = True
intents.messages = True
intents.guilds = True

bot = commands.Bot(command_prefix='/', intents=intents)


@bot.event
async def on_ready():
    print(f'logged in as {bot.user}')

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.application_id == bot.application_id:
        await bot.intents.commands.fetch_application_commands(bot.application_id)
        await bot.tree.process(interaction)

@tasks.loop(seconds=10.0)
async def start_music_player():
    for guild in bot.guilds:
        for voice_client in guild.voice_clients:
            if voice_client.is_playing():
                if not bot.is_paused:
                    await voice_client.continue_playing()
                else:
                    await voice_client.pause()
                    
bot.load_extension("cogs.ikiforgot

bot.is_paused = False

bot.run(token)