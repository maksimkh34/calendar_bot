# handler functions
import time
from afdef import *
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import pandas as pd
from event import event
# context.bot.send_message(update.effective_chat.id, "")
# def x(update, context):

def start(update, context):
    context.bot.send_message(update.effective_chat.id, "Это бот-календарь. Он может планировать события, изменять уже запланированные, и удалять их, но пока не может оповещать о их наступлении... \n\n"
                                                       "Команды бота: \n"
                                                       "/add - Бот добавит событие\n"
                                                       "/check - Бот выводит все запланированные события\n"
                                                       "/edit - Бот выводит все события, а затем можно изменить текст выбранного события\n"
                                                       "/delete - Бот удаляет выбранное событие\n"
                                                       "/about - Описание бота\n"
                                                       "/help или /start - Вывести этот список еще раз")

def showevents(update, context):
    context.bot.send_message(update.effective_chat.id, "Загрузка событий... ")
    events = importdb()
    for i in range(len(events)):
        context.bot.send_message(update.effective_chat.id,
            f"Событие на {events[i].year}.{events[i].month}.{events[i].day}, {events[i].hour}:{events[i].minute} - {events[i].event_name}")
    if len(events)==0: context.bot.send_message(update.effective_chat.id, "События не найдены!")
    Keyboard = [[InlineKeyboardButton("Добавить события", callback_data='3')]]
    context.bot.send_message(update.effective_chat.id, "Чтобы доавбить новые события, введите /add", reply_markup=InlineKeyboardMarkup(Keyboard))

def pressedhelp(update, context):
    query = update.callback_query
    query.answer()
    if query.data == '1':
        start(update, context)
    if query.data == '2':
        showevents(update, context)
    if query.data == '3':
        addevent(update, context)
    if query.data[0:4] == 'del_':
        print("presset to delete " + query.data[4])
        dbdf = pd.read_csv('db.csv')
        dbdf.drop(labels=[int(query.data[4])], axis = 0, inplace=True)
        dbdf.to_csv('db.csv')
        Keyboard = [[InlineKeyboardButton("Показать запланированные события", callback_data='2')]]
        if not(update.message==None):
            update.message.reply_text('Событие удалено. Введите /check для просмотра текущих событий', reply_markup=InlineKeyboardMarkup(Keyboard))
        else:
            context.bot.send_message(update.effective_chat.id,'Событие удалено. Введите /check для просмотра текущих событий', reply_markup=InlineKeyboardMarkup(Keyboard))
    if query.data[0:4] == 'edt_':
        data = query.data.split('_')
        indx = int(data[1])
        new_name = data[2]
        db = pd.read_csv('db.csv')
        db.at[indx, 'event'] = new_name
        db.to_csv('db.csv')
        Keyboard = [[InlineKeyboardButton("Показать запланированные события", callback_data='2')]]
        context.bot.send_message(update.effective_chat.id,'Событие изменено. Введите /check для просмотра текущих событий', reply_markup=InlineKeyboardMarkup(Keyboard))


def unknowncommand(update, context):
    Keyboard = [[InlineKeyboardButton("Показать команды", callback_data='1')]]
    update.message.reply_text("Команда не распознана. Введите /help, чтобы просмотреть все команды", reply_markup=InlineKeyboardMarkup(Keyboard))

def addevent(update, context):
    if (update.message == None) or (update.message.text == '/add'):
        context.bot.send_message(update.effective_chat.id, "Введите данные нового события в формате:\n /add YYYY.MM.DD HH:MM - Событие\n"
                                                           "Например: /add 2012.12.20 14:00 - День рождения")
    else:
        vnt = event(0, 0, 0, 0, 0, "")
        vnt = splitevent(update.message.text)
        if not(len(update.message.text)<25):
            if not(checkevent(vnt, context, update)):
                update.message.reply_text("Событие задано неверно. Введите /add для справки")
            else:
                dictevent = {'year':vnt.year, 'month':vnt.month, 'day':vnt.day, 'hour':vnt.hour, 'minute':vnt.minute, 'event':vnt.event_name}
                old_db = pd.read_csv('db.csv')
                new_db = old_db.append(dictevent, ignore_index=True)
                new_db.to_csv('db.csv')
                Keyboard = [[InlineKeyboardButton("Показать запланированные события", callback_data='2')]]
                update.message.reply_text("Событие успешно добавлено. Введите /check для просмотра текущих событий", reply_markup=InlineKeyboardMarkup(Keyboard))
        else:
            print("len inv")
            update.message.reply_text("Событие задано неверно. Введите /add для справки")
    evt = event(0, 0, 0, 0, 0, "")

def delete_event(update, context):
    events = importdb()
    Keyboard = []
    if len(events)==0:
        context.bot.send_message(update.effective_chat.id, "События не найдены! ")
    else:
        for i in range(len(events)):
            Keyboard.append([InlineKeyboardButton(f"{events[i].event_name} ({events[i].year}.{events[i].month}.{events[i].day}, {events[i].hour}:{events[i].minute})", callback_data='del_' + str(i))])
        update.message.reply_text("Какое событие требуется удалить? ",reply_markup=InlineKeyboardMarkup(Keyboard))

def about(update, context):
    context.bot.send_message(update.effective_chat.id, "Developed by https://github.com/maksimkh34\n"
                                                       "GitHub: https://github.com/maksimkh34/calendar_bot")

def editevent(update, context):
    events = importdb()
    Keyboard = []
    new_event_name = update.message.text[6:len(update.message.text)]
    if update.message.text == '/edit':
        update.message.reply_text("Команда используется в формате /edit 'Новое событие'. Текст какого события изменить можно выбрать после использования команды.")
    else:
        if len(events) == 0:
            context.bot.send_message(update.effective_chat.id, "События не найдены! ")
        else:
            for i in range(len(events)):
                Keyboard.append([InlineKeyboardButton(
                    f"{events[i].event_name} ({events[i].year}.{events[i].month}.{events[i].day}, {events[i].hour}:{events[i].minute})",
                    callback_data="edt_" + str(i) + "_" + update.message.text[5:len(update.message.text)]
                )])
            update.message.reply_text("Какое событие требуется изменить? ", reply_markup=InlineKeyboardMarkup(Keyboard))