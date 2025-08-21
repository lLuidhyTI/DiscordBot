# Discord Bot

This project is a Discord bot that allows users to interact with it through commands and manage music playback in voice channels.

## Files

- **src/Bot.py**: Contains the main code for the Discord bot. It initializes the bot, sets up commands for interacting with users, and manages music playback in voice channels. It includes classes and functions for handling music sessions, extracting YouTube information, and managing command responses.

- **.env**: This file is used to store environment variables, including the `DISCORD_TOKEN`, which is required for the bot to authenticate with the Discord API.

- **requirements.txt**: Lists the Python dependencies required for the project, including libraries such as `discord.py`, `yt-dlp`, and `python-dotenv`.

## Setup Instructions

1. **Clone the repository**:
   ```
   git clone <repository-url>
   cd discord-bot
   ```

2. **Create a virtual environment** (optional but recommended):
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install dependencies**:
   ```
   pip install -r requirements.txt
   ```

4. **Set up the environment variables**:
   Create a `.env` file in the root directory and add your Discord bot token:
   ```
   DISCORD_TOKEN=your_token_here
   ```

5. **Run the bot**:
   ```
   python src/Bot.py
   ```

## Usage

- Use the command prefix & to interact with the bot.
- Available commands include:
- &fenrir: Introduces the bot.
- &hi: Sends a good morning message with an embedded GIF.
- &join: Joins the user's voice channel.
- &leave: Leaves the voice channel.
- &play <url>: Plays a song or playlist from YouTube.
- &pause: Pauses the current song.
- &resume: Resumes the paused song.
- &skip: Skips the current song.
- &back: Goes back to the previous song.
- &queue: Displays the current song and the queue.

## Contributing

Feel free to submit issues or pull requests for improvements or bug fixes.

## Notes

- Make sure FFmpeg is installed and added to your system PATH, otherwise the bot will not be able to play audio.
- PyNaCl is required for voice/audio functionality, so ensure it is installed via requirements.txt.
