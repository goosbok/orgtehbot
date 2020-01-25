# coding: utf8
from telegram.ext import Updater
from telegram.ext import MessageHandler, CallbackQueryHandler, CommandHandler, Filters
# from telegram import InlineKeyboardMarkup, InlineKeyboardButton
# from telegram import KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove
# from telegram import File
import logging
# import time
# import os

token = '1038469498:AAGeQ16BovO3kVyr2PRUnVaruxDtFzzNVVY'
request_kwargs = {
    'proxy_url': 'socks5h://185.162.131.46:11084'
}
proxy_list = [
    '69.4.86.195:61901',
    '185.130.105.66:11084',
    '31.148.220.141:11084',
    '185.162.131.46:11084',
]


#############  bot  #############
chats = {
    'admins_group_chat_id':-353048395
}
### Commands_Handler ###                                                                ## обработчик команд
def start(bot, update):  # старт
    message = update.message
    name = message['chat']['first_name']
    bot.send_message(chat_id=message.chat_id,
                     text=otvet1(name),
                     reply_markup=askAQuestionKB())


### Message_Handler ###                                                                 ## обработчик сообщений
def message_handler(bot, update, group=None):
    message = update.message
    text = message.text
    chat_id = message.chat_id
    message_id = message.message_id
    name = message['chat']['first_name']
    if text == cancel['text']:
        bot.send_message(chat_id=chat_id,
                         text=otvet1(name),
                         reply_markup=askAQuestionKB())
        return
    if chat_id != chats['admins_group_chat_id']:
        bot.send_message(chat_id=chats['admins_group_chat_id'],
                         text=group)
        bot.forward_message(chat_id=chats['admins_group_chat_id'],
                            from_chat_id=chat_id,
                            message_id=message_id,
                            )
        bot.send_message(chat_id=chat_id,
                         text=otvet3())
    elif (chat_id == chats['admins_group_chat_id'] or chat_id == chats['rent_group_chat_id']) and update.message.reply_to_message:
        bot.forward_message(chat_id=update.message.reply_to_message.forward_from.id,
                            from_chat_id=update.message.reply_to_message.forward_from.id,
                            message_id=message.reply_to_message.message_id-1)
        bot.send_message(chat_id=update.message.reply_to_message.forward_from.id,
                         text=f'Ответ:\n{text}')


### Callback_Handler ###

def callback_handler(bot, update):                                                  ## обработчик команд
    query = update.callback_query
    data = query.data
    chat_id = query.message.chat_id
    message_id = query.message.message_id
    if data == ask_a_question_support['callback_data']:
        bot.delete_message(chat_id=chat_id,
                           message_id=message_id)
        bot.send_message(chat_id=chat_id,
                         text=otvet2(),
                         reply_markup=cancelKB())
        message_handler(bot,updater.update_queue.get(),group='Общий вопрос:')
    elif data == ask_a_question_rent['callback_data']:
        bot.delete_message(chat_id=chat_id,
                           message_id=message_id)
        bot.send_message(chat_id=chat_id,
                         text=otvet_rent(),
                         reply_markup=cancelKB())
        bot.send_message(chat_id=chat_id,
                         text=otvet2())
        message_handler(bot, updater.update_queue.get(),group='Аренда:')
### Other func ###


#############  keyboard  #############
### keys ###
instagrams = {
    'text': 'Instagram логины из VK',
    'callback_data': 'instagrams'
}
ask_a_question_support = {
    'text':'Обслуживание оргтехники 📠',
    'callback_data':'question'
}
ask_a_question_rent = {
    'text':'Партнёрство по Аренде 💶',
    'callback_data':'rent'
}
cancel = {
    'text':'Отмена',
    'callback_data':'cancel'
}

### KBs ###
def askAQuestionKB ():
    keyboard = [
        [InlineKeyboardButton(text=ask_a_question_support['text'], callback_data=ask_a_question_support['callback_data'])],
        [InlineKeyboardButton(text=ask_a_question_rent['text'],callback_data=ask_a_question_rent['callback_data'])]
    ]
    return InlineKeyboardMarkup(keyboard)

def cancelKB():
    keyboard = [
        [KeyboardButton(text=cancel['text'])]
    ]
    return ReplyKeyboardMarkup(keyboard,one_time_keyboard=True,resize_keyboard=True)
#############  message  #############
def main_menu_message():
    return 'Отправьте сообщение для тех.поддержки:'
def otvet1(name):
    return f'Добрый день, {name}!\n\nМеня зовут Clara, я электронный ассистент ГК Оргтехника Плюс!\n\nЧем погу помочь?'
def otvet2():
    return 'Убедительная просьба, сформулируйте Ваш вопрос в одном сообщении и отправьте мне, я передам его тех.поддержке.'
def otvet3():
    return 'Я передала Ваш вопрос администрации Оргтехника Плюс! Очень скоро Вы получите ответ!'
def otvet_rent():
    return 'В данном разделе Вы можете стать нашим партнёром по предоставлению оргтехники в аренду и получить всю необходимую информацию.\n\n'
#############  handler  #############
updater = Updater(token=token)#,
                  #request_kwargs=request_kwargs)
updater.dispatcher.add_handler(CommandHandler('start', start))
updater.dispatcher.add_handler(CallbackQueryHandler(callback_handler))
updater.dispatcher.add_handler(MessageHandler(Filters.text, message_handler))
updater.start_polling()
#############  logger  #############
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
