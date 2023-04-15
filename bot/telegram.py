#!/usr/bin/python
# library-bot


import telebot
from telebot import types
from dbapi import *


token = '6044586998:AAFd-FQB_7n0-fk_8R8go3zCmSruejydnYI'

bot = telebot.TeleBot(token)

book_data = {'name' : '', 'author' : '', 'year' : 0}

# handle commands
cmds = ['start', 'help', 'add', 'delete', 'list', 'find', 'borrow', 'retrieve', 'stats']

@bot.message_handler(commands=cmds)
def send_welcome(message):
    if message.text.lower() == '/start':
        bot.send_message(message.from_user.id, """Добро пожаловать в чат бота-библиотеки!\n\nНапишите /help для вывода команд.""")

    elif message.text.lower() == '/help':
        return help_handler(message)

    elif message.text.lower() == '/add':
        return add_handler(message)
        
    elif message.text.lower() == '/delete':
        return delete_handler(message)

    elif message.text.lower() == '/list':
        return list_handler(message)

    elif message.text.lower() == '/find':
        return find_handler(message)

    elif message.text.lower() == '/borrow':
        return borrow_handler(message)

    elif message.text.lower() == '/retrieve':
        return retrieve_handler(message)

    elif message.text.lower() == '/stats':
        return stats_handler(message)


# filter for callback answers
@bot.callback_query_handler(func=lambda call: True)
def answer(call):
    if 'del' in call.data:
        if call.data == 'del_yes':
            try:
                delete()
                bot.send_message(call.message.chat.id, 'Книга удалена')
            except:
                bot.send_message(call.message.chat.id, "Невозможно удалить книгу")
        elif call.data == 'del_no':
            pass
    if 'brw' in call.data:
        if call.data == 'brw_yes':
            borrow()
            # вы взяли эту книгу / эту книгу нельзя взять
        elif call.data == 'brw_no':
            pass


def help_handler(message):
    bot.send_message(message.from_user.id, """\
/start    -    начать
/add      -    добавить книгу 
/delete   -    удалить книгу
/list     -    вывести список книг
/find     -    найти книгу
/borrow   -    взять книгу
/retrieve -    вернуть книгу
/stats    -    получить статистику по книге
""")
                       

# /add
def add_handler(message):
    msg = bot.send_message(message.from_user.id, "Введите название книги:")
    bot.register_next_step_handler(msg, add_book_name_handler)


def add_book_name_handler(message):
    book_data['name'] = message.text
    msg = bot.send_message(message.from_user.id, "Введите автора:")
    bot.register_next_step_handler(msg, add_author_handler)
    

def add_author_handler(message):
    book_data['author'] = message.text
    msg = bot.send_message(message.from_user.id, "Введите год издания:")
    bot.register_next_step_handler(msg, add_published_handler)


def add_published_handler(message):
    try:
        book_data['year'] = int(message.text)
        # метод из dbapi
        add()
        bot.reply_to(message, f"Книга добавлена (id)\n{repr(book_data)}")
    except ValueError:
        bot.reply_to(message, "Ошибка при добавлении книги")
        msg = bot.send_message(message.from_user.id, "Введите год издания:")
        bot.register_next_step_handler(msg, add_published_handler)


# /delete
def delete_handler(message):
    msg = bot.send_message(message.from_user.id, "Введите название книги:")
    bot.register_next_step_handler(msg, delete_book_name_handler)


def delete_book_name_handler(message):
    book_data['name'] = message.text
    msg = bot.send_message(message.from_user.id, "Введите автора:")
    bot.register_next_step_handler(msg, delete_author_handler)


def delete_author_handler(message):
    book_data['author'] = message.text
    msg = bot.send_message(message.from_user.id, "Введите год издания:")
    bot.register_next_step_handler(msg, delete_published_handler)


def delete_published_handler(message):
    # проверка на ввод года
    try:
        book_data['year'] = int(message.text)
    except ValueError:
        bot.reply_to(message, "Ошибка, неверный формат года")
        msg = bot.send_message(message.from_user.id, "Введите год издания:")
        bot.register_next_step_handler(msg, delete_published_handler) 

    markup = types.InlineKeyboardMarkup(one_time=True)

    markup.add(
        types.InlineKeyboardButton(text='Да', callback_data='del_yes'),
        types.InlineKeyboardButton(text='Нет', callback_data='del_no'),
    )
    
    bot.send_message(message.chat.id, f"Найдена книга: {book_data['name']} {book_data['author']} {book_data['year']}. Удаляем?", reply_markup=markup)


# /list
def list_handler(message):
    # ну тут чисто обращение к бдшке и вывод
    pass


# /find
def find_handler(message):
    msg = bot.send_message(message.from_user.id, "Введите название книги:")
    bot.register_next_step_handler(msg, find_name_handler)


def find_name_handler(message):
    # добавь в базу данных объект message.text
    book_data['name'] = message.text
    msg = bot.send_message(message.from_user.id, "Введите автора:")
    bot.register_next_step_handler(msg, find_author_handler)
    

def find_author_handler(message):
    # добавь в базу данных объект message.text
    book_data['author'] = message.text
    msg = bot.send_message(message.from_user.id, "Введите год издания:")
    bot.register_next_step_handler(msg, find_published_handler)


def find_published_handler(message):
    try:
        book_data['year'] = int(message.text)
    except ValueError:
        msg = bot.send_message(message.chat.id, "Ошибка, неверный формат года")
        bot.register_next_step_handler(msg, find_published_handler)

    find()
    # найдено/не найдено


# /borrow
def borrow_handler(message):
    msg = bot.send_message(message.from_user.id, "Введите название книги:")
    bot.register_next_step_handler(msg, borrow_book_handler)


def borrow_book_handler(message):
    book_data['name'] = message.text
    msg = bot.send_message(message.from_user.id, "Введите автора:")
    bot.register_next_step_handler(msg, borrow_author_handler)


def borrow_author_handler(message):
    book_data['author'] = message.text
    msg = bot.send_message(message.from_user.id, "Введите год издания:")
    bot.register_next_step_handler(msg, borrow_published_handler)


def borrow_published_handler(message):
    # проверка на ввод года
    try:
        book_data['year'] = int(message.text)
    except ValueError:
        bot.reply_to(message, "Ошибка, неверный формат года")
        msg = bot.send_message(message.from_user.id, "Введите год издания:")
        bot.register_next_step_handler(msg, borrow_published_handler) 

    markup = types.InlineKeyboardMarkup(one_time=True)

    markup.add(
        types.InlineKeyboardButton(text='Да', callback_data='brw_yes'),
        types.InlineKeyboardButton(text='Нет', callback_data='brw_no'),
    )
    
    bot.send_message(message.chat.id, f"Найдена книга: {book_data['name']} {book_data['author']} {book_data['year']}. Берем?", reply_markup=markup)


# /retrieve
def retrieve_handler(message):
    retrieved_book = retrieve()
    bot.send_message(message.chat.id, f"Вы вернули книгу {retrieved_book}")


# /stats
def stats_handler(message):
    msg = bot.send_message(message.from_user.id, "Введите название книги:")
    bot.register_next_step_handler(msg, stats_name_handler)


def stats_name_handler(message):
    # добавь в базу данных объект message.text
    book_data['name'] = message.text
    msg = bot.send_message(message.from_user.id, "Введите автора:")
    bot.register_next_step_handler(msg, stats_author_handler)
    

def stats_author_handler(message):
    # добавь в базу данных объект message.text
    book_data['author'] = message.text
    msg = bot.send_message(message.from_user.id, "Введите год издания:")
    bot.register_next_step_handler(msg, stats_published_handler)


def stats_published_handler(message):
    try:
        book_data['year'] = int(message.text)
    except ValueError:
        msg = bot.send_message(message.chat.id, "Ошибка, неверный формат года")
        bot.register_next_step_handler(msg, stats_published_handler)

    stats()

bot.polling(non_stop=True, interval=0)