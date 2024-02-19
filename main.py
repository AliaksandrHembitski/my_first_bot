import telebot

from config import TOKEH, keys
from extensions import APIException, CheckingDataConverter

bot = telebot.TeleBot(TOKEH)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = ('Чтобы начать работу введите команду боту в следующем формате:\n'
            '<наименование валюты, стоимость которой нужно узнать> <наименование валюты, в которую нужно перевести стоимость искомой валюты>'
            '<количество искомой валюты>'
            'название валют пишем без угловых скобок, с маленькой буквы, через один пробел между параметрами'
            ' в конце запроса пробел не ставим'
            '\nУвидеть список всех доступных валют можно введя команду: /values')
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')
    try:
        CheckingDataConverter.checking_data(values)
        text = CheckingDataConverter.get_price(values)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n {e}')
    else:
        bot.send_message(message.chat.id, text)


bot.polling()

