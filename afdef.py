from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import pandas as pd
from event import event


def splitevent(text):
    list1 = text.split(' ')
    eventname = ""
    for i in range(4, len(list1)):
        eventname += list1[i] + ' '

    date = list1[1].split('.')
    year = date[0]
    month = date[1]
    day = date[2]

    time_ = list1[2].split(':')
    hour = time_[0]
    minute = time_[1]
    vnt = event(year, month, day, hour, minute, eventname)
    return vnt


def checkevent(vnt, context, update):
    if int(vnt.year)>3000 or int(vnt.year)<2022:
        print("year invalid")
        context.bot.send_message(update.effective_chat.id, f"Год указан неверно ({vnt.year})")
    elif int(vnt.month) <= 0 or int(vnt.month) > 12:
        context.bot.send_message(update.effective_chat.id, f"Месяц указан неверно ({vnt.month})")
        return False
    elif int(vnt.day) <= 0 or int(vnt.day) > 31:
        context.bot.send_message(update.effective_chat.id, f"День указан неверно ({vnt.day})")
        return False
    elif int(vnt.hour) < 0 or int(vnt.hour) > 24:
        context.bot.send_message(update.effective_chat.id, f"Час указан неверно ({vnt.hour})")
        return False
    elif int(vnt.minute) < 0 or int(vnt.minute) > 60:
        context.bot.send_message(update.effective_chat.id, f"Минута указана неверно ({vnt.minute})")
        return False
    else:
        return True


def importdb():
    dbase = pd.read_csv("db.csv")
    events = []
    years = dbase['year'].tolist()
    months = dbase['month'].tolist()
    days = dbase['day'].tolist()
    hours = dbase['hour'].tolist()
    minutes = dbase['minute'].tolist()
    events_names = dbase['event'].tolist()
    for i in range(len(dbase)):
        x = event(years[i], months[i], days[i], hours[i], minutes[i], events_names[i])
        events.append(x)
    return events