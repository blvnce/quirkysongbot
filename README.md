# 🎵 QuirkySongBot

A Discord music bot built with Python that allows users to search for and play music directly in a Discord voice channel.

This project was created as a personal programming project to practice Python, Discord bot development, APIs, queues, and audio playback.

## Features

* 🎵 Search and play songs using `/play`
* ⏭️ Skip the current song with `/skip`
* 📋 View the current music queue with `/queue`
* 🔊 Automatically play queued songs
* 🔗 Automatically join the user's voice channel
* 👋 Leave the voice channel with `/leave`
* 🏓 Test the bot with `/ping`

## Commands

| Command        | Description                                 |
| -------------- | ------------------------------------------- |
| `/ping`        | Check if the bot is online                  |
| `/join`        | Join the user's voice channel               |
| `/play <song>` | Search for and play a song                  |
| `/queue`       | Display the current music queue             |
| `/skip`        | Skip the current song                       |
| `/leave`       | Leave the voice channel and clear the queue |

## Technologies

* Python
* discord.py
* yt-dlp
* FFmpeg
* PyNaCl
* python-dotenv

## How It Works

The bot uses Discord's API through `discord.py` to receive slash commands.

When `/play` is used, the bot searches for the requested song using `yt-dlp`. The resulting audio URL is passed to FFmpeg, which streams the audio through Discord's voice connection.

Songs requested while another song is playing are stored in a queue. When the current song finishes, the bot automatically takes the next song from the queue and starts playing it.

## Project Structure

```text
quirkysongbot/
├── bot.py
├── requirements.txt
├── README.md
└── .gitignore
```

## Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd quirkysongbot
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file

Create a file named `.env` and add your Discord bot token:

```env
DISCORD_TOKEN=your_bot_token_here
```

**Never upload your `.env` file or Discord bot token to GitHub.**

### 4. Run the bot

```bash
python bot.py
```

## What I Learned

Through this project, I practiced:

* Python functions and asynchronous programming
* Discord slash commands
* Voice channel connections
* Audio streaming with FFmpeg
* Queue management
* Environment variables and `.env` files
* Debugging package and dependency issues
* Using Git and GitHub for project management

## Future Improvements

Possible future features include:

* 🔊 Volume controls
* 🎶 Now-playing information
* 🗑️ Queue management
* 🔁 Repeat/loop functionality
* 🎛️ Better error handling
* 🏠 Separate queues for different Discord servers
* 🧩 Splitting the project into multiple Python modules
