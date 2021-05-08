import discord
from . import utils, command_handlers, database

class Bot:
    command_database = {
        "default": "me",
        "commands": {
            "me": {
                "aliases": ["m"],
                "description": "Shows statistics about you. Use with a username to set your Minecraft account."
            },
            "username": {
                "aliases": ["u"],
                "description": "Shows statistics about the player with the given username."
            },
            "past": {
                "aliases": ["p"],
                "description": "Shows all statistics collected by the bot about you over time."
            },
            "future": {
                "aliases": ["f"],
                "description": "Shows information about stats at a date or statistic in the future. Uses your username if none is passed.\n" +
                "Valid suffixes are `d` (days), `mo` (months), `y` (years), `*` (stars), `fkdr`, `wlr`, `bblr`, `fk` (final kills), `w` (wins), `b` (beds).\n" +
                "Fetch your statistics regularly for accurate predictions. (Statistics fetched for a username by anyone using any command are factored into any prediction for that username.)"
            },
            "help": {
                "aliases": ["h"],
                "description": "Displays this help message on how to use the bot."
            }
        }
    }
    default_storage = {
        "discord_user_ids_to_minecraft_uuids": {},
        "minecraft_uuids": {},
        "errors": []
    }
    def __init__ (self, *, config):
        self.config = config
        self.client = discord.Client ()
        self.client.event (self.on_message)
        self.storage = database.Database (intent = "storage", file_name = self.config ["storage_file_name"], default = self.default_storage)
    def run (self):
        self.client.run (self.config ["discord_bot_token"], bot = self.config ["discord_is_bot"])
    async def on_message (self, message: discord.Message):
        if message.author.id == self.client.user.id: return
        is_command, command, args = utils.simplify_command (message_content = message.content, prefix = self.config ["prefix"])
        if not is_command: return
        found_command, execution_success = await utils.resolve_prefixes_and_exec (command_database = self.command_database, command = command, args = [self, message, *args], execution_target = command_handlers.CommandHandlers)
        if not found_command: await message.reply ("Command not found!")