import discord
from discord.ext import commands
import asyncio

with open('token.txt') as inpf:
    token = inpf.readline()

# client = discord.Client()
bot = commands.Bot(command_prefix='!')

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.command()
async def q(ctx, arg):
    await ctx.send(arg)

@bot.command()
async def joinVoice(ctx):
    if (ctx.author.voice): # Check if author of the command is in voice channel
        if not (ctx.voice_client): # Check if Friday is not already in voice channel
            voiceChannel = ctx.author.voice.channel
            await voiceChannel.connect()
            await ctx.send('Joined voice channel: "' + str(voiceChannel.name) + '"')
        else:
            await ctx.send('Friday already is in voice channel, use !leaveVoice')
    else:
        await ctx.send("Join voice channel to invite Friday")

@bot.command()
async def leaveVoice(ctx): # Note: ?leave won't work, only ?~ will work unless you change  `name = ["~"]` to `aliases = ["~"]` so both can work.
    if (ctx.voice_client): # If the bot is in a voice channel 
        await ctx.guild.voice_client.disconnect() # Leave the channel
        await ctx.send('Left voice channel')
    else: # But if it isn't
        await ctx.send("I'm not in voice channel")

@bot.command()# TODO
async def playSmth(ctx):
    await ctx.send('Attempting to play')
    audio_source = discord.FFmpegPCMAudio('content/audio/Ohayo.mp3')
    if (ctx.voice_client):
        ctx.voice_client.play(audio_source)

@bot.event
async def on_voice_state_update(member, before, after):
    voiceClient = discord.utils.get(bot.voice_clients, guild=member.guild)
    if ((before.channel is None) and (voiceClient is not None) and (after.channel == voiceClient.channel)):
        audio_source = discord.FFmpegPCMAudio('content/audio/Ohayo.mp3')
        await asyncio.sleep(1)
        voiceClient.play(audio_source)
                 

@bot.command()
async def shutdown(ctx):
    if str(ctx.author.top_role) == "Кирилл":
        await ctx.send('Shutting down...Done.')
        await bot.close()
    else:
        await ctx.send('Только Кирилл может меня выключить, позови его.')

    
bot.run(token)