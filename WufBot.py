from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import logging
import re
import config
import urllib.request as URLreq
import json

TOKEN = config.token
OWNER_ID = config.owner_id

# ???? something to do with exception handling / logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

# Updater receives updates from telegram and delivers them to dispatcher.
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher


##########
# /START #
##########
def start(bot, update):
    bot.sendMessage(update.message.chat_id, text="Hey, welcome! I'm " + bot.name + "!\n\n" +
                                                 "I don't do much right now. But I can repeat your messages " +
                                                 "back to you. \n\nI can also yell at you. I've been practicing. " +
                                                 "To get me to yell something, type /yell followed by a message.\n\n" +
                                                 "Please note that for testing purposes, messages sent to this bot " +
                                                 "will be visible to the bot owner, @icedog25.")


# on /start command, run the start function. (str command, function)
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

#########
# /HELP #
#########
help_handler = CommandHandler('help', start)
dispatcher.add_handler(help_handler)


##############
# Forwarding #
##############
def forward_me(bot, update):
    bot.forwardMessage(chat_id=OWNER_ID, from_chat_id=update.message.chat_id,
                       message_id=update.message.message_id, disable_notification=True)


########################
# Text Message Echoing #
########################
def echo(bot, update):
    forward_me(bot, update)
    bot.sendMessage(chat_id=update.message.chat_id, text=update.message.text)


# Filters.text is a filter for only text messages.
echo_handler = MessageHandler(Filters.text, echo)
dispatcher.add_handler(echo_handler)


#########
# /YELL #
#########
def yell(bot, update, args):
    # join uses ' ' to separate elements in args (list).
    text_yell = loudify(' '.join(args).upper())
    forward_me(bot, update)
    bot.sendMessage(chat_id=update.message.chat_id, text=text_yell)

COMMAND = 0
PHRASE = 1

def loudify(string):
    return re.sub(
        '[?]','?!', re.sub('[.!]+','!!!', string)
         ).upper() + '!!!'


yell_handler = CommandHandler('yell', yell, pass_args=True)
dispatcher.add_handler(yell_handler)


def cat(bot, update):
    forward_me(bot, update)

    with URLreq.urlopen("https://api.thecatapi.com/v1/images/search") as url:
        data = json.loads(url.read().decode())
        img_url = data[0]['url']
        bot.send_photo(chat_id=update.message.chat_id, photo=img_url)


cat_handler = CommandHandler('cat', cat)
dispatcher.add_handler(cat_handler)

################
# STARTING BOT #
################
updater.bot.sendMessage(OWNER_ID, "The bot has been initialized!")
updater.start_polling()
