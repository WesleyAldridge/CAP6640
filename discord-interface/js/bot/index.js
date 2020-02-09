require('dotenv').config();
const Discord = require('discord.js');
const bot = new Discord.Client();

bot.on('ready', () => {
    console.log(`Logged in as ${bot.user.tag}!`)
})

bot.on('message', msg => {
    if (msg.content === 'Hello') {
        msg.reply('Hello!');
    }
    if (msg.content === 'Hate') {
        msg.reply('Please be kind!');
    }
})

bot.login(process.env.BOT_TOKEN);
