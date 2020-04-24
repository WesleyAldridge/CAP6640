from .discord_bot import discord_bot

class setup_bot:
    def read_token_file(self, file):
        credFile = open(file)
        self.token = credFile.read()
        credFile.close()

    def start(self):
        client = discord_bot()
        client.run(self.token)

