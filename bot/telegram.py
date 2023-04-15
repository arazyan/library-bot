#!/usr/bin/python
# asynchronic library-bot


from telebot.async_telebot import AsyncTeleBot
from config import token
bot = AsyncTeleBot(token)


# Handle '/start' and '/help'
cmds = ['start', 'help', 'add', 'delete', 'list', 'find', 'borrow', 'retrieve', 'stats']
@bot.message_handler(commands=cmds)
async def send_welcome(message):
    if message.text.lower() == '/start':
        await bot.reply_to(message, """\
    Добро пожаловать в чат бота-библиотеки!\n\nНапишите /help для вывода команд.
    """)
    elif message.text.lower() == '/help':
        return await help_handler(message)


async def help_handler(message):
    await bot.reply_to(message, """\
/start    -    начать
/add      -    добавить книгу 
/delete   -    удалить книгу
/list     -    вывести список книг
/find     -    найти книгу
/borrow   -    взять книгу
/retrieve -    вернуть книгу
/stats    -    получить статистику по книге
""")
                       




import asyncio
asyncio.run(bot.polling(none_stop=True, interval=0))