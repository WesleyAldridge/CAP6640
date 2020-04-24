import sys
from bot.setup_bot import setup_bot

# Instantiate class for dealing with bot
bot = setup_bot()

# Tries to read token from token.txt if token file name is not provided
if len(sys.argv) != 2:
    try:
        bot.read_token_file('token.txt')
    except FileNotFoundError:
        print("usage: python3 main.py <token_file>")
        exit()

# Otherwise read the provided file
else:
    bot.read_token_file(str(sys.argv[1]))

# Run bot
bot.start()

