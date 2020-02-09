import discord
import sys

# we would import here and use model to classify inbound messages

def usage():
    print("usage: python3 main.py <token_file>")

if len(sys.argv) != 2:
    usage()
    exit()

credFile = open(str(sys.argv[1]))
token = credFile.read()
credFile.close()

class HaterOfHaters(discord.Client):
    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))

client = HaterOfHaters()
client.run(token)