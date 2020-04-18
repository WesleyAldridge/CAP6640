import discord
from classifier.hate_classifier import hate_classifier

classifier = hate_classifier()

class discord_bot(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        is_hate_message = classifier.predict(message)
        print('Classifier Message:' + str(is_hate_message))
        if is_hate_message:
            self
