import pprint
import telebot
import json
import requests
from bs4 import BeautifulSoup

TOKEN = '5793648640:AAFtlMVMlnoty-rrzIEPZqLWP8RXVyU-w8Q'

# bot name Tev15Telebot

MAIN_URL = f'https://api.telegram.org/bot{TOKEN}'

# Информация о боте
url = f'{MAIN_URL}/getMe'

print(url)

proxies = {
    'http': 'http://167.86.96.4:3128',
    'https': 'http://167.86.96.4:3128',
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.117 Safari/537.36'
}

with open('parced_data.json', 'r', encoding='utf-8') as datafile:
    posts = json.load(datafile)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    message_txt = """Вас приветсвует telbot15. \nКоманды: \n/review - обзор публикаций \n/view ДАТА - публикации на ДАТУ \n/header ДАТА - заголовки на ДАТУ"""
    bot.send_message(message.chat.id, message_txt)


# Обзор всех дат публикаций
@bot.message_handler(commands=['review'])
def review(message):
    for post in posts:
        bot.send_message(message.chat.id, post[0])

# вывод url публикаций по дате
@bot.message_handler(commands=['view'])
def view(message):
    post_found = False
    param = ' '.join(message.text.split(' ')[1:])
    for post in posts:
        if post[0] == param:
            post_found = True
            bot.reply_to(message, post[1])
    if not post_found:
        bot.reply_to(message, f'Нет записей на дату {param.upper()}!')
        bot.reply_to(message, f'Посмотрите список командой /review')

# Вывод заголовка публикации по дате
@bot.message_handler(commands=['headers'])
def header(message):
    post_found = False
    param = ' '.join(message.text.split(' ')[1:])
    for post in posts:
        if post[0] == param:
            post_found = True
            url_post = post[1]
            response1 = requests.get(url_post)
            soup = BeautifulSoup(response1.content, 'html.parser')
            page = soup.find('h1', class_='alignwide wp-block-post-title')
            bot.reply_to(message, page.text.strip().upper())
    if not post_found:
        bot.reply_to(message, f'Нет записей на дату {param.upper()}!')
        bot.reply_to(message, f'Посмотрите список дат:')
        review(message)

# Проверка вывода картинки из файла
@bot.message_handler(commands=['relax'])
def relax_foto(message):
    with open('foto1.jpg', 'rb') as data:
        bot.send_photo(message.chat.id, data)


bot.polling()




