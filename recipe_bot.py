import telebot
from telebot import types
import random
import json
token="5371708856:AAFjSjtyderlCBeg05W2K1FKXNAVLEQaDKg"
bot=telebot.TeleBot(token)
f = open('Завтраки.json', 'r', encoding='UTF-8')
recipe_1 = json.load(f)
f.close()
f = open('Обеды.json', 'r', encoding='UTF-8')
recipe_2 = json.load(f)
f.close()
f = open('Ужины.json', 'r', encoding='UTF-8')
recipe_3 = json.load(f)
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
        markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
        item2=types.KeyboardButton("Завтраки")
        item3=types.KeyboardButton("Обеды")
        item4=types.KeyboardButton("Ужины")
        markup.add(item2)
        markup.add(item3)
        markup.add(item4)
        bot.send_message(message.chat.id, 'Нажми: \nНа какой прием пищи вы хотите получить рецепт ',  reply_markup=markup)
    if  message.text.strip() == 'Завтраки' :
        answer = str(random.choice(recipe_1))
        bot.send_message(message.chat.id, answer)
    elif message.text.strip() == 'Обеды' :
        answer = str(random.choice(recipe_2))
        bot.send_message(message.chat.id, answer)
    elif message.text.strip() == 'Ужины':
        answer = str(random.choice(recipe_3))
        bot.send_message(message.chat.id, answer)

bot.polling(none_stop=True, interval=0)
