import StatsHomie.config, StatsHomie.bot

def main (argv):
    default_config_file_name = "config.json"
    config_file_name = argv [0] if len (argv) > 0 else default_config_file_name
    config = StatsHomie.config.Config (file_name = config_file_name)
    bot = StatsHomie.bot.Bot (config = config)
    bot.run ()

if __name__ == "__main__":
    import sys
    main (sys.argv)
