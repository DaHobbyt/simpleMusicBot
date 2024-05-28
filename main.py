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



@bot.tree.command(name='join', description='Join voice channel')
async def join(interaction: discord.Interaction):
    if not interaction.user.voice:
        await interaction.response.send_message("You are not connected to a voice channel!", ephemeral=True)
        return
    else:
        channel = interaction.user.voice.channel
    await channel.connect()
    await interaction.response.send_message("Connected to the voice channel!", ephemeral=True)

@bot.tree.command(name='play', description='Play music')
async def play(interaction: discord.Interaction, url: str):
    await interaction.response.send_message("Playing...", ephemeral=True)
    voice_client = interaction.guild.voice_client
    async with interaction.typing():
        player = await youtube_dl.YoutubeDL({}).extract_info(url, download=False)
        voice_client.play(discord.FFmpegPCMAudio(player['formats'][0]['url']))

@bot.tree.command(name='pause', description='Pause music')
async def pause(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if voice_client.is_playing():
        bot.is_paused = True
        voice_client.pause()
        await interaction.response.send_message("Paused", ephemeral=True)
    else:
        await interaction.response.send_message("Currently not playing music", ephemeral=True)

@bot.tree.command(name='resume', description='Resume music')
async def resume(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    if bot.is_paused:
        voice_client.resume()
        bot.is_paused = False
        await interaction.response.send_message("Resumed", ephemeral=True)
    else:
        await interaction.response.send_message("Currently not playing music or not paused", ephemeral=True)

@bot.tree.command(name='stop', description='Stop music')
async def stop(interaction: discord.Interaction):
    voice_client = interaction.guild.voice_client
    bot.is_playing = False
    bot.is_paused = False
    voice_client.stop()
    await interaction.response.send_message("Stopped", ephemeral=True)

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

bot.is_paused = False

bot.run(token)