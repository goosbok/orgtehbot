# coding: utf8
from telegram.ext import Updater
from telegram.ext import MessageHandler, CallbackQueryHandler, CommandHandler, Filters
from telegram import Message
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram import File
import logging
import time
import os
from last_mes import last_mes

token = '1038469498:AAGeQ16BovO3kVyr2PRUnVaruxDtFzzNVVY'
request_kwargs = {
    'proxy_url': 'socks5h://185.162.131.46:11084'
}

admins_group_chat_id = -353048395
proxy_list = [
    '69.4.86.195:61901',
    '185.130.105.66:11084',
    '31.148.220.141:11084',
    '185.162.131.46:11084',
]


#############  bot  #############
### Commands_Handler ###                                                                ## обработчик команд
def start(bot, update):  # старт
    message = update.message
    bot.send_message(chat_id=message.chat_id,
                     text=otvet1())
    bot.send_message(chat_id=message.chat_id,
                     text=otvet2())


### Message_Handler ###                                                                 ## обработчик сообщений
def message_handler(bot, update):
    message = update.message
    text = message.text
    chat_id = message.chat_id
    message_id = message.message_id
    print(message)
    if chat_id != admins_group_chat_id:
        bot.forward_message(chat_id=admins_group_chat_id,
                            from_chat_id=chat_id,
                            message_id=message_id
                            )
        # bot.delete_message(chat_id=chat_id,
        #                    message_id=message_id-1)
        bot.send_message(chat_id=chat_id,
                         text=otvet3())
    elif chat_id == admins_group_chat_id and update.message.reply_to_message:
        bot.forward_message(chat_id=update.message.reply_to_message.forward_from.id,
                            from_chat_id=update.message.reply_to_message.forward_from.id,
                            message_id=message.reply_to_message.message_id-1)
        bot.send_message(chat_id=update.message.reply_to_message.forward_from.id,
                         text=f'Ответ:\n{text}')

    # if (last_mes[f'{chat_id}'] - message.date) < 10:



### Callback_Handler ###

def callback_handler(bot, update):                                                  ## обработчик команд
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id

### Other func ###


#############  keyboard  #############
### keys ###
instagrams = {'text': 'Instagram логины из VK',
              'callback_data': 'instagrams'}


### KBs ###

#############  message  #############
def main_menu_message():
    return 'Отправьте сообщение для тех.поддержки:'
def otvet1():
    return 'Добрый день, Уважаемый партнёр!\n\nМеня зовут Clara, я электронный ассистент ГК Оргтехника Плюс!\n\nКакой у Вас вопрос?'
def otvet2():
    return 'Убедительная просьба, формулируйте Ваш вопрос в одном сообщении.'
def otvet3():
    return 'Я передала Ваш вопрос администрации Оргтехника Плюс! Очень скоро Вы получите ответ!'
#############  handler  #############
updater = Updater(token=token,
                  request_kwargs=request_kwargs)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))
updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
updater.start_polling()
#############  logger  #############
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
