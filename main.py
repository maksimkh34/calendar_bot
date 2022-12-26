from telegram import Update, Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackQueryHandler
from const import bot_token
from handler_functions import *
from datetime import datetime
import pandas as pd
from event import event

# initializating bot
bot = Bot(bot_token)
updater = Updater(bot_token, use_context=True)
dispatcher = updater.dispatcher
d = datetime.now()
print(f"Bot initializated. ({d.time().hour}:{d.time().minute}:{d.time().second})")

# handlers
button_help_handler = CallbackQueryHandler(pressedhelp)
start_handler = CommandHandler('start', start)
help_handler = CommandHandler('help', start)
unknown_handler = MessageHandler(Filters.command, unknowncommand)
showevents_handler = CommandHandler('check', showevents)
add_handler = CommandHandler('add', addevent)
deleteevent_handler = CommandHandler('delete', delete_event)
about_handler = CommandHandler('about', about)
editevent_handler = CommandHandler('edit', editevent)

# adding handlers
dispatcher.add_handler(start_handler)
dispatcher.add_handler(help_handler)
dispatcher.add_handler(button_help_handler)
dispatcher.add_handler(showevents_handler)
dispatcher.add_handler(add_handler)
dispatcher.add_handler(deleteevent_handler)
dispatcher.add_handler(about_handler)
dispatcher.add_handler(editevent_handler)

# default handlers
dispatcher.add_handler(unknown_handler)


# starting polling
print("Polling started... ")
updater.start_polling()
updater.idle()
print("Stopped.")

