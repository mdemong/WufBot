from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
import logging
import re

TOKEN = '356457602:AAEpx13fbbqoR_Nb4IKpn6SUxhRJ5eW3kQU'
ICEDOG_USERID = '92366006'

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
    bot.forwardMessage(chat_id=ICEDOG_USERID, from_chat_id=update.message.chat_id,
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
# def yell(bot, update, args):
#     # join uses ' ' to separate elements in args (list).
#     text_yell = ' '.join(args).upper() + "!!!"
#     forward_me(bot, update)
#     bot.sendMessage(chat_id=update.message.chat_id, text=text_yell)

COMMAND = 0
PHRASE = 1

def loudify(string):
    return re.sub(
        '[?]','?!', re.sub('[.!]+','!!!', string)
         ).upper() + '!!!'

def request_yell_text():



def yell(bot, update, args):
    forward_me(bot, update)
    if (args.length > 0):
        # takes msg text, chops off 0th word, preserves the rest of the string
        removed_slash = update.message.text.split((' '),1)[1]
        text_yell = loudify(removed_slash)
        bot.sendMessage(chat_id=update.message.chat_id, text=text_yell)
    else:
        text_yell = loudify(request_yell_text())
        bot.sendMessage(chat_id=update.message.chat_id,text=text_yell)




yell_conv_handler = ConversationHandler(
    entry_points=[CommandHandler('yell', yell)],
    states={
        COMMAND: [],


    }
)
dispatcher.add_handler(yell_conv_handler)

################
# STARTING BOT #
################
updater.bot.sendMessage(ICEDOG_USERID, "The bot has been initialized!")
updater.start_polling()