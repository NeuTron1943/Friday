import discord
from discord.ext import commands
import asyncio
from gtts import gTTS
import logging
import os


# read secret token from file :) conspiracy
with open('token.txt') as inpf:
    token = inpf.readline()

#create logging system
log_handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True


# class MyBot(discord.Client):
class MyBot(commands.Bot):
    def __init__(self, **kwargs):
        super(MyBot, self).__init__(**kwargs)

    async def on_ready(self):
        print(f'Logged on as {self.user}!')

    async def on_message(self, message):
        print(f'Message log:   {message.author} :   {message.content}')
        if message.author == self.user:
            return

        await self.process_commands(message)


bot = MyBot(command_prefix='!', intents=intents)

# Test command for texting arguments
@bot.command()
async def q(ctx, arg):
    await ctx.send(arg)

# Turn off the bot
@bot.command()
async def shutdown(ctx):
    if str(ctx.author.top_role) == "Кирилл":
        await ctx.send('Shutting down...Done.')
        await bot.close()
    else:
        await ctx.send('Только Кирилл может меня выключить, позови его.')
    
# join same voice channel, as the author of the command
@bot.command()
async def joinVoice(ctx):
    print("Here 1")
    if (ctx.author.voice): # Check if author of the command is in voice channel
        print("Here 2")
        if not (ctx.voice_client): # Check if Friday is not already in voice channel
            print("Here 3")
            voiceChannel = ctx.author.voice.channel
            print("Here 34")
            await voiceChannel.connect()
            print("Here 4")
            await ctx.send('Joined voice channel: "' + str(voiceChannel.name) + '"')
        else:
            print("Here 5")
            await ctx.send('Friday already is in voice channel, use !leaveVoice')
    else:
        print("Here 6")
        await ctx.send("Join voice channel to invite Friday")
    print("Here 7")

# leave current voice channel
@bot.command()
async def leaveVoice(ctx): # Note: ?leave won't work, only ?~ will work unless you change  `name = ["~"]` to `aliases = ["~"]` so both can work.
    if (ctx.voice_client): # If the bot is in a voice channel 
        await ctx.guild.voice_client.disconnect() # Leave the channel
        await ctx.send('Left voice channel')
    else: # But if it isn't
        await ctx.send("I'm not in voice channel")



bot.run(token, log_handler=log_handler, log_level=logging.DEBUG)