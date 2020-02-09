require('dotenv').config();
const Discord = require('discord.js');
const bot = new Discord.Client();

bot.on('ready', () => {
    console.log(`Logged in as ${bot.user.tag}!`)
});

bot.on('message', msg => {
    if (msg.content === 'Hello') {
        msg.reply('Hello!');
    }
    if (msg.content === 'Hate') {
        msg.reply('Please be kind!');
    }
    if (msg.content.startsWith('!kick')) {
        const member = msg.mentions.members.first()

        if (!member) {
            return msg.reply(
                `Who are you trying to kick? You must mention a user.`
            )
        }

        if (!member.kickable) {
            return msg.reply(`I can't kick this user. Sorry!`)
        }

        return member
            .kick()
            .then(() => msg.reply(`${member.user.tag} was kicked.`))
            .catch(error => msg.reply(`Sorry, an error occured.`))
    }
});

bot.on('guildMemberAdd', member => {
    member.send(
        `Welcome on the server! Please be aware that we won't hate speech or harassment. Have fun 😀`
    );
});

bot.login(process.env.BOT_TOKEN);
