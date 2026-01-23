# ValoRecap.py

A Discord bot that provides detailed Valorant match statistics and automatic match tracking using the Valorant API.

## Features

- **Match Breakdown** - Get detailed statistics and visualizations for any Valorant player's most recent match
- **Match Tracking** - Automatically track and post match results for specified 
- **Random Generation** - Looking to have some fun? Use the bot to generate a random crosshair, gun loadout, or agent for you to play with!

## Commands

- `/match <name> <tag>` - Get a detailed breakdown of the most recent match for a player
- `/track <name> <tag>` - Start tracking a player's matches in the current channel
- `/untrack <name> <tag>` - Stop tracking a player's matches
- `/agent` - Generate a random agent
- `/gun` - Generate a random gun loadout
- `/crosshair` - Generate a random crosshair profile

## Prerequisites

- Python 3.8 or higher
- Discord Bot Token
- Henrik Dev Valorant API Key

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/ValoRecap.py.git
cd ValoRecap.py
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

3. Configure the bot:
   - Open [main.py](main.py)
   - Replace `<DISCORD BOT TOKEN HERE>` with your Discord bot token
   - Replace `<HDEV API KEY HERE>` with your Henrik Dev API key

4. Update debug guilds (optional):
   - In [main.py](main.py), replace the guild IDs in the `debug_guilds` parameter with your server IDs

## Running the Bot

```bash
python main.py
```

The bot will log in and start monitoring for slash commands and tracked matches.

## Project Structure

```
ValoRecap.py/
├── main.py                 # Bot entry point and core setup
├── requirements.txt        # Python dependencies
├── assets/
│   └── fonts/             # Custom fonts for match graphics
├── cogs/                  # Discord.py command modules
│   ├── agent.py          # Agent information commands
│   ├── crosshair.py      # Crosshair commands
│   ├── gun.py            # Weapon information commands
│   ├── match.py          # Match breakdown commands
│   ├── track.py          # Match tracking commands
│   └── untrack.py        # Untrack commands
└── matchResults/          # Match result processing
    ├── check_recent_matchs.py
    └── match_results.py   # Match graphic generation
```

## API Keys

### Discord Bot Token
1. Go to the [Discord Developer Portal](https://discord.com/developers/applications)
2. Create a new application
3. Go to the "Bot" section
4. Create a bot and copy the token

### Henrik Dev API Key
1. Visit [Henrik Dev's Valorant API](https://docs.henrikdev.xyz/)
2. Request an API key
3. Use the key in your configuration

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- [Henrik Dev Valorant API](https://github.com/Henrik-3/unofficial-valorant-api) for providing Valorant data
- [Valorant-API.com](https://valorant-api.com/) for asset data

### Font Attributions

The following fonts are used in match graphics generation:

- **Airborne II Pilot** by Charles Casimiro (airbrne2.ttf) - Used for player names and statistics
- **Falling Sky** by Paul D. Hunt (FallingSky-JKwK.otf) - Used for headers and titles
- **Falling Sky Bold Plus** by Paul D. Hunt (FallingSkyBoldplus-6GZ1.otf) - Used for emphasized text and scores

All fonts are used in accordance with their respective licenses.

## Support

For issues, questions, or suggestions, please open an issue on the GitHub repository.

## Disclaimer

This project is not affiliated with Riot Games. Valorant and all associated properties are trademarks or registered trademarks of Riot Games, Inc.
