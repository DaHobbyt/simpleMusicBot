import discord
from discord.ext import commands
import youtube_dl

class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.is_playing = False
        self.is_paused = False

    @commands.slash_command(name="join", description="makes the bot join ur voice channel")
    async def join(self, ctx):
        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel!")
            return
        else:
            channel = ctx.message.author.voice.channel
        await channel.connect()

    @commands.slash_command(name="play", description="plays a song")
    async def play(self, ctx, url):
        server = ctx.message.guild
        voice_channel = server.voice_client

        async with ctx.typing():
            player = await youtube_dl.YoutubeDL({}).extract_info(url, download=False)
            voice_channel.play(discord.FFmpegPCMAudio(player['formats'][0]['url']))
            await ctx.send('Playing...')

    @commands.slash_command(name="pause", description="Pauses a song")
    async def pause(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if voice_client.is_playing():
            self.is_paused = True
            voice_client.pause()
            await ctx.send("Paused")
        else:
            await ctx.send("Currently not playing music")

    @commands.slash_command(name="resume", description="resumes the song")
    async def resume(self, ctx):
        voice_client = ctx.message.guild.voice_client
        if self.is_paused:
            voice_client.resume()
            self.is_paused = False
            await ctx.send("Resumed")
        else:
            await ctx.send("Currently not playing music or not paused")

    @commands.slash_command(name="stop", description="stops the bot")
    async def stop(self, ctx):
        voice_client = ctx.message.guild.voice_client
        self.is_playing = False
        self.is_paused = False
        voice_client.stop()
        await ctx.send("Stopped")

def setup(bot):
    bot.add_cog(Music(bot))