import telebot
from telebot import types
import random
token="5371708856:AAFjSjtyderlCBeg05W2K1FKXNAVLEQaDKg"
bot=telebot.TeleBot(token)
f = open('recipe.txt', 'r', encoding='UTF-8')
recipe = f.read().split('\n')
f.close()
@bot.message_handler(commands=["start"])
def start(m, res=False):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1=types.KeyboardButton("Рецепт")	
    markup.add(item1)
    bot.send_message(m.chat.id, 'Нажми: \nРецепт для получения рецепт ',  reply_markup=markup)
@bot.message_handler(content_types=["text"])
def handle_text(message):
    if message.text.strip() == 'Рецепт' :
        answer = random.choice(recipe)
    bot.send_message(message.chat.id, answer)
bot.polling(none_stop=True, interval=0)
