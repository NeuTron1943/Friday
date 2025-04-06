import discord
from discord.ext import commands
from gtts import gTTS
import os
import yt_dlp as youtube_dl

# read secret token from file :) conspiracy
with open('token.txt') as inpf:
    token = inpf.readline()

AUDIO_PATH = 'C:/Projects/Friday/content/audio/'
ydl_opts = {
    'format': 'bestaudio/best',
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
    'outtmpl': 'downloads/%(title)s.%(ext)s',
}
# Включаем необходимые разрешения
intents = discord.Intents.default()
intents.message_content = True

# Создаем экземпляр бота с префиксом команд
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command()
async def q(ctx, *, text: str):
    """Дублирует указанный текст"""
    await ctx.send(text)


# Turn off the bot
@bot.command()
async def shutdown(ctx):
    if str(ctx.author.top_role) == "Кирилл":
        await ctx.send('Shutting down...Done.')
        await bot.close()
    else:
        await ctx.send('Только Кирилл может меня выключить, позови его.')

@bot.command()
async def joinVoice(ctx):
    """Подключает бота к голосовому каналу"""
    # Проверяем, находится ли пользователь в голосовом канале
    if not ctx.author.voice:
        await ctx.send("Сначала зайдите в голосовой канал!")
        return

    # Получаем канал пользователя
    channel = ctx.author.voice.channel

    # Проверяем, подключен ли бот уже к голосовому каналу
    if ctx.voice_client:
        # Если бот уже в канале пользователя
        if ctx.voice_client.channel == channel:
            await ctx.send("Я уже в вашем голосовом канале!")
        else:
            # Если бот в другом канале, перемещаемся
            await ctx.voice_client.move_to(channel)
            await ctx.send(f"Переместился в канал {channel.name}!")
    else:
        # Если бот не подключен, подключаемся
        await channel.connect()
        await ctx.send(f"Подключился к каналу {channel.name}!")

@bot.command()
async def playAudio(ctx, *, path: str):
    """Воспроизводит аудиофайл из указанного пути"""
    global current_player
    
    path = os.path.join(AUDIO_PATH, path)
    print(f'Attemting to play {path}')
    # Проверка существования файла
    if not os.path.exists(path):
        await ctx.send("Файл не найден!")
        return

    # Проверка подключения к голосовому каналу
    if not ctx.voice_client:
        await ctx.invoke(bot.get_command('joinVoice'))

    # Останавливаем текущее воспроизведение
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    # Создаем аудио источник
    source = discord.FFmpegPCMAudio(executable="ffmpeg", source=path)
    current_player = ctx.voice_client.play(source)
    await ctx.send(f"Начинаю воспроизведение: {path}")

@bot.command()
async def stop(ctx):
    """Останавливает текущее воспроизведение"""
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Воспроизведение остановлено!")
    else:
        await ctx.send("Сейчас ничего не играет!")    

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        ytdl = youtube_dl.YoutubeDL(ydl_opts)
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        
        if 'entries' in data:
            data = data['entries'][0]
        
        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename), data=data)

@bot.command()
async def youtube(ctx, url: str):
    """Воспроизводит аудио с YouTube"""
    if not ctx.author.voice:
        await ctx.send("Сначала зайдите в голосовой канал!")
        return

    # Подключаемся к каналу если не подключены
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()

    # Создаем аудио источник
    player = await YTDLSource.from_url(url, loop=bot.loop, stream=True)
    
    # Останавливаем текущее воспроизведение
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    ctx.voice_client.play(player, after=lambda e: print(f'Ошибка: {e}') if e else None)
    await ctx.send(f"Сейчас играет: {player.title}")

@q.error
async def quote_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Добавьте текст после команды! Пример: `!q Привет!`")

@joinVoice.error
async def join_error(ctx, error):
    if isinstance(error, commands.CommandError):
        await ctx.send("Ошибка подключения! Проверьте права бота")

# Обработчики ошибок
@playAudio.error
async def play_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Укажите путь к файлу! Пример: `!play music.mp3`")


bot.run(token)