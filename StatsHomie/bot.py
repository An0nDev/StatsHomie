import discord

class Bot:
    def __init__ (self, *, config):
        self.config = config
        self.client = discord.Client ()
        self.client.event (self.on_message)
    def run (self):
        self.client.run (self.config ["discord_bot_token"], bot = self.config ["discord_is_bot"])
    async def on_message (self, message):
        if message.content.startswith (self.config ["prefix"]):
            print (message)