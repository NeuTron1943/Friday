import discord
from discord.ext import commands
import asyncio
from gtts import gTTS
import os

# read secret token from file :) conspiracy
with open('token.txt') as inpf:
    token = inpf.readline()


# client = discord.Client()
bot = commands.Bot(command_prefix='!')


# event occurs when bot logges into server
@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))


# test command, writes arg in same chat
@bot.command()
async def q(ctx, arg):
    await ctx.send(arg)


# join same voice channel, as the author of the command
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


# leave current voice channel
@bot.command()
async def leaveVoice(ctx): # Note: ?leave won't work, only ?~ will work unless you change  `name = ["~"]` to `aliases = ["~"]` so both can work.
    if (ctx.voice_client): # If the bot is in a voice channel 
        await ctx.guild.voice_client.disconnect() # Leave the channel
        await ctx.send('Left voice channel')
    else: # But if it isn't
        await ctx.send("I'm not in voice channel")


# playing sound
'''
@bot.command()# TODO
async def playSmth(ctx):
    await ctx.send('Attempting to play')
    audio_source = discord.FFmpegPCMAudio('content/audio/Ohayo.mp3')
    if (bot.voice_clients):
        bot.voice_clients[0].play(audio_source)
    else:
        await ctx.send('Friday is not connected to voice channel')
'''


# pronouncing sentence of any length
@bot.command()
async def say(ctx, *args):
    voiceline = ''
    for arg in args:
        voiceline += str(arg)
        voiceline += " "
    # await ctx.send('Saying')
    tmp_path = 'content/audio/tmp/voiceline.mp3'
    narrator = gTTS(text=voiceline, lang='ru', slow=False)
    narrator.save(tmp_path)

    audio_source = discord.FFmpegPCMAudio(tmp_path)
    # if (ctx.voice_client):
        # ctx.voice_client.play(audio_source)
    if (bot.voice_clients):
        bot.voice_clients[0].play(audio_source)
    else:
        await ctx.send('Friday is not connected to voice channel')
        


# play Ohayo when someone entered same voice channel
@bot.event
async def on_voice_state_update(member, before, after):
    voiceClient = discord.utils.get(bot.voice_clients, guild=member.guild)
    if ((before.channel is None) and (voiceClient is not None) and (after.channel == voiceClient.channel)):
        audio_source = discord.FFmpegPCMAudio('content/audio/Ohayo.mp3')
        await asyncio.sleep(1)
        voiceClient.play(audio_source)
                 

# shutdown bot
@bot.command()
async def shutdown(ctx):
    if str(ctx.author.top_role) == "Кирилл":
        await ctx.send('Shutting down...Done.')
        await bot.close()
    else:
        await ctx.send('Только Кирилл может меня выключить, позови его.')


# running bot
bot.run(token)