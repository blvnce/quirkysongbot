from multiprocessing.util import info
import os

import discord
import yt_dlp
from discord.ext import commands
from dotenv import load_dotenv


music_queue = []

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

intents = discord.Intents.default()

bot = commands.Bot(
    command_prefix="!",
    intents=intents
)


@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} command(s)")
    except Exception as e:
        print(f"Failed to sync commands: {e}")


@bot.tree.command(name="ping", description="Check if the bot is working")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message("🏓 Pong!")


@bot.tree.command(name="join", description="Join your voice channel")
async def join(interaction: discord.Interaction):

    # Check if the user is in a voice channel
    if not interaction.user.voice:
        await interaction.response.send_message(
            "❌ You need to join a voice channel first."
        )
        return

    voice_channel = interaction.user.voice.channel

    # Check if the bot is already connected
    if interaction.guild.voice_client:
        await interaction.guild.voice_client.move_to(voice_channel)
    else:
        await voice_channel.connect()

    await interaction.response.send_message(
        f"🎵 Joined **{voice_channel.name}**!"
    )

def play_next(voice_client, error=None):

    if error:
        print(f"Playback error: {error}")

    if not music_queue:
        return

    next_song = music_queue.pop(0)

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(next_song["webpage_url"], download=False)

    audio_url = info["url"]

    audio_source = discord.FFmpegPCMAudio(audio_url)

    voice_client.play(
        audio_source,
        after=lambda error: play_next(voice_client, error)
    )

@bot.tree.command(name="play", description="Search and play a song")
async def play(interaction: discord.Interaction, song: str):

    await interaction.response.defer()

    if not interaction.user.voice:
        await interaction.followup.send(
            "❌ You need to join a voice channel first."
        )
        return

    voice_channel = interaction.user.voice.channel

    if interaction.guild.voice_client:
        voice_client = interaction.guild.voice_client
    else:
        voice_client = await voice_channel.connect()

    ydl_opts = {
        "format": "bestaudio/best",
        "quiet": True,
        "default_search": "ytsearch",
        "noplaylist": True,
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(song, download=False)

    if "entries" in info:
        info = info["entries"][0]

    title = info.get("title", "Unknown")
    audio_url = info["url"]

    song_info = {
        "title": title,
        "webpage_url": info["webpage_url"]
    }

    if voice_client.is_playing():
        music_queue.append(song_info)

        await interaction.followup.send(
            f"➕ Added to queue: **{title}**"
        )
        return

    audio_source = discord.FFmpegPCMAudio(audio_url)

    voice_client.play(
        audio_source,
        after=lambda error: play_next(voice_client, error)
    )

    await interaction.followup.send(
        f"🎵 Now playing: **{title}**"
    )

@bot.tree.command(name="queue", description="Show the current music queue")
async def queue(interaction: discord.Interaction):

    if not music_queue:
        await interaction.response.send_message(
            "📭 The queue is empty."
        )
        return

    queue_text = "🎵 **Music Queue:**\n\n"

    for index, song in enumerate(music_queue, start=1):
        queue_text += f"**{index}.** {song['title']}\n"

    await interaction.response.send_message(queue_text)


@bot.tree.command(name="skip", description="Skip the current song")
async def skip(interaction: discord.Interaction):

    voice_client = interaction.guild.voice_client

    if not voice_client or not voice_client.is_playing():
        await interaction.response.send_message(
            "❌ Nothing is currently playing."
        )
        return

    voice_client.stop()

    await interaction.response.send_message(
        "⏭️ Skipped the current song."
    )


@bot.tree.command(name="leave", description="Leave the voice channel")
async def leave(interaction: discord.Interaction):

    voice_client = interaction.guild.voice_client

    if not voice_client:
        await interaction.response.send_message(
            "❌ I'm not in a voice channel."
        )
        return

    music_queue.clear()
    await voice_client.disconnect()

    await interaction.response.send_message(
        "👋 Left the voice channel."
    )


if not TOKEN:
    raise RuntimeError("DISCORD_TOKEN was not found.")


bot.run(TOKEN)
