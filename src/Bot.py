import discord
import os
import yt_dlp
import asyncio
import functools
from discord.ext import commands
from dotenv import load_dotenv
from collections import deque

# Carregar variáveis do .env
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# Configuração intents
intents = discord.Intents.all()
bot = commands.Bot("&", intents=intents)

# Inicializando o bot
@bot.event
async def on_ready():
    print("🤖 Bot inicializado com sucesso!")

# Comandos
@bot.command()
async def fenrir(ctx: commands.Context):
    await ctx.send(
        "Olá, sou Fenrir, um bot programado por *Luidhy* para praticar conceitos de programação em Python."
    )

@bot.command()
async def hi(ctx: commands.Context):
    hi_embed = discord.Embed()
    hi_embed.title = "Bom Dia"
    imagem = discord.File("imagens/Makise.gif","Makise.gif")
    hi_embed.set_image(url="attachment://Makise.gif")

    await ctx.reply(embed=hi_embed, file=imagem)


# --- Sistema de música ---
class GuildMusic:
    def __init__(self):
        self.queue = deque()   # [(url, title)]
        self.history = deque() # [(url, title)]
        self.vc = None

    def add_song(self, url, title):
        self.queue.append((url, title))

    def current_song(self):
        return self.history[-1] if self.history else None


# Sessões por guild
music_sessions = {}  # {guild_id: GuildMusic}


# --- Extrair info do YouTube ---
def yt_extract(url):
    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "skip_download": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        return ydl.extract_info(url, download=False)


async def get_stream_info(url):
    loop = asyncio.get_event_loop()
    info = await loop.run_in_executor(None, functools.partial(yt_extract, url))
    stream_url = info.get("url")
    title = info.get("title", "Título desconhecido")
    return stream_url, title


# --- Entrar no canal de voz ---
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        vc = await channel.connect()
        music_sessions[ctx.guild.id] = GuildMusic()
        music_sessions[ctx.guild.id].vc = vc
        await ctx.send(f"🎵 Conectado em {channel.name}")
    else:
        await ctx.send("❌ Você precisa estar em um canal de voz primeiro!")


# --- Sair do canal de voz ---
@bot.command()
async def leave(ctx):
    session = music_sessions.get(ctx.guild.id)
    if session and session.vc:
        await session.vc.disconnect()
        del music_sessions[ctx.guild.id]
        await ctx.send("👋 Desconectado do canal de voz")
    else:
        await ctx.send("❌ O bot não está conectado em nenhum canal")


# --- Função para tocar música ---
async def play_music(ctx, url, title, send_msg=True):
    guild_id = ctx.guild.id
    session = music_sessions.get(guild_id)

    if not session:
        session = GuildMusic()
        music_sessions[guild_id] = session

    if not session.vc:
        if ctx.author.voice:
            channel = ctx.author.voice.channel
            session.vc = await channel.connect()
        else:
            if send_msg:
                await ctx.send("❌ Você precisa estar em um canal de voz primeiro!")
            return

    vc = session.vc

    # Função chamada quando a música termina
    def after_play(error):
        if error:
            print(f"Erro no player: {error}")
        fut = asyncio.run_coroutine_threadsafe(play_next(ctx), bot.loop)
        try:
            fut.result()
        except Exception as e:
            print(f"Erro futuro: {e}")

    # Função assíncrona para tocar a próxima música
    async def play_next(ctx):
        if session.queue:
            try:
                next_url, next_title = session.queue.popleft()
                session.history.append((next_url, next_title))
                stream_url, _ = await get_stream_info(next_url)

                vc.play(
                    discord.FFmpegPCMAudio(
                        stream_url,
                        before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                        options="-vn",
                    ),
                    after=after_play,
                )
                await ctx.send(f"▶️ Tocando agora: **{next_title}**")
            except Exception as e:
                print(f"Erro ao tocar próxima música: {e}")
                await ctx.send(f"❌ Erro ao tocar próxima música: {e}")

    # Adiciona à fila
    session.add_song(url, title)

    # Se nada estiver tocando, toca imediatamente
    if not vc.is_playing() and not vc.is_paused():
        next_url, next_title = session.queue.popleft()
        session.history.append((next_url, next_title))
        try:
            stream_url, _ = await get_stream_info(next_url)
            vc.play(
                discord.FFmpegPCMAudio(
                    stream_url,
                    before_options="-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                    options="-vn",
                ),
                after=after_play,
            )
            if send_msg:
                await ctx.send(f"▶️ Tocando agora: **{next_title}**")
        except Exception as e:
            if send_msg:
                await ctx.send(f"❌ Erro ao tocar música: {e}")


# --- Comando play ---
@bot.command()
async def play(ctx, url):
    loop = asyncio.get_event_loop()

    # Extrair vídeos de playlist ou único
    def extract_urls(url):
        ydl_opts = {
            "format": "bestaudio/best",
            "quiet": True,
            "extract_flat": "in_playlist",
            "skip_download": True,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)
        if "entries" in info:
            return [
                (e.get("url"), e.get("title"))
                for e in info["entries"]
                if e
            ]
        else:
            return [(info.get("url"), info.get("title"))]

    try:
        urls = await loop.run_in_executor(None, functools.partial(extract_urls, url))
    except Exception as e:
        await ctx.send(f"❌ Erro ao extrair informações do YouTube: {e}")
        return

    if not urls:
        await ctx.send("❌ Nenhuma música encontrada no link fornecido.")
        return

    for video_url, title in urls:
        await play_music(ctx, video_url, title, send_msg=False)

    if len(urls) > 1:
        await ctx.send(f"✅ Playlist adicionada à fila ({len(urls)} músicas)")
    else:
        await ctx.send(f"✅ Música adicionada à fila")


# --- Comando pause ---
@bot.command()
async def pause(ctx):
    session = music_sessions.get(ctx.guild.id)
    if session and session.vc and session.vc.is_playing():
        session.vc.pause()
        await ctx.send("⏸ Música pausada!")


# --- Comando resume ---
@bot.command()
async def resume(ctx):
    session = music_sessions.get(ctx.guild.id)
    if session and session.vc and session.vc.is_paused():
        session.vc.resume()
        await ctx.send("▶️ Música continuada!")


# --- Comando skip ---
@bot.command()
async def skip(ctx):
    session = music_sessions.get(ctx.guild.id)
    if session and session.vc and session.vc.is_playing():
        session.vc.stop()
        await ctx.send("⏭ Música pulada!")


# --- Comando back ---
@bot.command()
async def back(ctx):
    session = music_sessions.get(ctx.guild.id)
    if not session or len(session.history) < 2:
        await ctx.send("❌ Não há música anterior para voltar!")
        return

    current = session.history.pop()
    prev_url, prev_title = session.history.pop()
    session.queue.appendleft(current)
    await play_music(ctx, prev_url, prev_title, send_msg=True)


# --- Comando queue ---
@bot.command()
async def queue(ctx):
    session = music_sessions.get(ctx.guild.id)
    if not session or (not session.queue and not session.history):
        await ctx.send("❌ Não há músicas na fila!")
        return

    msg = ""
    if session.history:
        _, current_title = session.current_song()
        msg += f"🎶 Tocando agora: **{current_title}**\n\n"

    if session.queue:
        msg += "📜 Próximas na fila:\n"
        for i, (_, title) in enumerate(session.queue, start=1):
            if i > 10:
                msg += f"... e mais {len(session.queue)-10} músicas\n"
                break
            msg += f"{i}. {title}\n"

    await ctx.send(msg)


# --- Tratamento para comandos inválidos ---
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("❌ Comando inválido!")
    else:
        raise error
 
# Iniciar bot
if DISCORD_TOKEN:
    bot.run(DISCORD_TOKEN)
else:
    print("❌ Erro: DISCORD_TOKEN não encontrado no arquivo .env")
