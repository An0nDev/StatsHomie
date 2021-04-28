import StatsHomie.database, StatsHomie.bot

def main (argv):
    default_config_file_name = "config.json"
    default_config = {
        "discord_bot_token": None,
        "discord_is_bot": True,
        "hypixel_api_key": None,
        "prefix": "sh",
        "storage_file_name": "storage.json",
        "host_discord_user_id": None
    }
    config_file_name = argv [1] if len (argv) > 1 else default_config_file_name
    config = StatsHomie.database.Database (intent = "config", file_name = config_file_name, default = default_config)
    bot = StatsHomie.bot.Bot (config = config)
    bot.run ()

if __name__ == "__main__":
    import sys
    main (sys.argv)
