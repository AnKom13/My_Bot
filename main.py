import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConv

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help', '1', ])
def send_welcome(message):
    bot.send_message(message.chat.id, f"Привет, {message.chat.username}")
    txt = 'Инструкция: \n введите сообщение вида <имя валюты (что переводите)> ' \
          '<имя валюты (во что переводите)> <количество> \n' \
          'Например: доллар рубль 10\n' \
          'Чтобы узнать список доступных валют нажмите /values'
    #    bot.reply_to(message,txt) #'вопрос'+сообщение
    bot.send_message(message.chat.id, txt)  # просто сообщение


@bot.message_handler(commands=['values', ])
def values(message):
    txt = 'Доступно:'
    for k in keys.keys():
        txt = '\n'.join([txt, k, ])
    bot.reply_to(message, txt)


@bot.message_handler(content_types=['text', ])
def convert(message):
    try:
        values = message.text.split()
        if len(values) != 3:
            raise APIException('Неверное число параметров. Должно быть 3.')
        what, where, how = values
        ans = CryptoConv.get_price(what, where, how)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя. \n {e}')
    except Exception as e:
        bot.reply_to(message, f'Ошибка сервера. \n {e}')
    else:
        out = f'Цена {how} {what} в {where} - {ans}'
        bot.send_message(message.chat.id, out)


bot.polling(none_stop=True)


