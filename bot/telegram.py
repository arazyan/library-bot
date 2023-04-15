#!/usr/bin/python
# library-bot


import telebot
from telebot import types

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

    book, author, year = '', '', ''


def add_book_name_handler(message):
    # добавь в базу данных объект message.text
    book_data['name'] = message.text
    msg = bot.send_message(message.from_user.id, "Введите автора:")
    bot.register_next_step_handler(msg, add_author_handler)
    

def add_author_handler(message):
    # добавь в базу данных объект message.text
    book_data['author'] = message.text
    msg = bot.send_message(message.from_user.id, "Введите год издания:")
    bot.register_next_step_handler(msg, add_published_handler)


def add_published_handler(message):
    try:
        book_data['year'] = int(message.text)
        # генерируй айди книги
        bot.reply_to(message, f"Книга добавлена (id)\n{repr(book_data)}")
        # добавь в бд данные book_add_data
    except ValueError:
        bot.reply_to(message, "Ошибка при добавлении книги")
        msg = bot.send_message(message.from_user.id, "Введите год издания:")
        bot.register_next_step_handler(msg, add_published_handler)


bot.polling(non_stop=True, interval=0)