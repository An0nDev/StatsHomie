# StatsHomie
A Discord bot written in Python that shows statistics and future predictions for Hypixel BedWars players.
Written and maintained by An0nDev#5162.
## Troubleshooting/Feedback
Text to @An0nDev#5162 or leave an issue in this repo. Thanks!
## Usage
Add the bot to your server or host your own (see Setup below) and type `sh.h` for a detailed help message.
## Setup
### Using the officially-hosted bot (recommended)
This bot is automatically updated when the repo is updated and runs 24/7.
To add it to your Discord server, use the following join link:
https://discord.com/oauth2/authorize?client_id=836580439690182656&scope=bot
### Hosting your own
- Install at least Python 3.8 (download from python.org or using your distro's package manager)
- Use `pip` to install the latest versions of dependencies (`pip3` if you also have Python 2 installed):
```
pip install discord.py requests --upgrade
```
- Clone the repository:
```
git clone https://github.com/An0nDev/StatsHomie && cd StatsHomie
```
- Create a file called `config.json` in the created folder `StatsHomie` and populate with the following information:
```json
{
  "discord_bot_token": "DISCORD_BOT_TOKEN_HERE",
  "discord_is_bot": true,
  "hypixel_api_key": "HYPIXEL_API_KEY_HERE",
  "prefix": "sh",
  "storage_file_name": "storage.json",
  "host_discord_user_id": 199195868400713729
}
```
`discord_bot_token` needs to be the token from Discord Developers associated with your bot.

`discord_is_bot` indicates whether the token is for a user (false) or for a bot (true).

`hypixel_api_key` needs to be a valid key for the Hypixel API, generated by running `/api` in chat.

`prefix` is whatever text needs to come before the name of the command for the bot to be activated.

`storage_file_name` is the name of the file used to store player data and Minecraft UUIDs of Discord users.

`host_discord_user_id` is the ID of the user that hosts the bot, as shown in the help message (`sh.h`).
- Run the bot (use `python3` if you also have Python 2 installed):
```shell
python main.py 
```