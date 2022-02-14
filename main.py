import discord
from discord.ext import commands

with open('token.txt') as inpf:
    token = inpf.readline()

# client = discord.Client()
client = commands.Bot(command_prefix='!')

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

@client.command()
async def q(ctx, arg):
    print(ctx.author.voice)
    await ctx.send(arg)

@client.command()
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

@client.command(aliases = ["~"])
async def leaveVoice(ctx): # Note: ?leave won't work, only ?~ will work unless you change  `name = ["~"]` to `aliases = ["~"]` so both can work.
    if (ctx.voice_client): # If the bot is in a voice channel 
        await ctx.guild.voice_client.disconnect() # Leave the channel
        await ctx.send('Left voice channel')
    else: # But if it isn't
        await ctx.send("I'm not in voice channel")

@client.command()
async def shutdown(ctx):
    if str(ctx.author.top_role) == "Кирилл":
        await ctx.send('Shutting down...Done.')
        await client.close()
    else:
        await ctx.send('Только Кирилл может меня выключить, позови его.')

'''
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    # if message.content.startswith('!q'):
        # await message.channel.send('Hi')

    if message.content.startswith('!shutdown'):
        await message.channel.send('Shutting down...Bye.')
        await client.close()'''
    
client.run(token)