import discord
from classifier.hate_classifier_tf_5050_lstm import hate_classifier

classifier = hate_classifier()
haters = {};

threshold = 0.85

class discord_bot(discord.Client):

    async def on_ready(self):
        print('Logged on as {0}!'.format(self.user))

    async def on_message(self, message):
        print('Message from {0.author}: {0.content}'.format(message))
        msg = False
        # Do not classify its own messages
        if message.author != self.user:
            if message.content=='.reset_hate_count':
                haters[message.author] = 0
                msg = 'Your count was reset, {0.author.mention}!'
            else:
                prediction = classifier.predict(message.content)
                print(message.content)
                is_hate_message = prediction >= threshold
                msg_classifier = 'Classifier: %s (%s)' % (prediction, is_hate_message)
                msg = ''
                if is_hate_message:
                    hate_messages = haters.get(message.author, 0) + 1
                    haters[message.author] = hate_messages
                    if hate_messages == 1:
                        msg = 'Please be kind {0.author.mention}!'
                    elif hate_messages == 2:
                        msg = 'This is not funny, {0.author.mention}! Please be kind otherwise I am kicking you!'
                    elif hate_messages == 3:
                        msg = 'Last warning! Another message like that and I kick you, {0.author.mention}.'
                    else:
                        msg = 'Your were kicked {0.author.mention}! (Hmm... not really but I could)'
                        # We don't effectively kick users but we could
                        # await self.kick(message.user.id);
                    print(msg.format(message))
                # Add the classifier output as debugging
                msg = msg + '\n' + msg_classifier
            if msg:
                await message.channel.send(msg.format(message))
