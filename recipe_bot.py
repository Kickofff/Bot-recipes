import telebot
from telebot import types
import random
import json
token="5371708856:AAFjSjtyderlCBeg05W2K1FKXNAVLEQaDKg"
bot=telebot.TeleBot(token)
f = open('recipes.json', 'r', encoding='UTF-8')
recipes = json.load(f)
f.close()
breakfast = []
lunch = []
dinner = []
for i in range(len(recipes)):
    if "Завтраки" in recipes[i]["eating"]:
        breakfast.append(recipes[i])
    if "Обеды" in recipes[i]["eating"]:
        lunch.append(recipes[i])
    if "Ужины" in recipes[i]["eating"]:
        dinner.append(recipes[i])
        
                
def json_recipe_to_str(r):
    return f'*Блюдо:* {r["name"]}.\n*Состав:* {", ".join(r["ingredients"])}.\n*Алгоритм Приготовления:* {r["recipe"]}'.replace(".", "\.")

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
        answer = json_recipe_to_str(random.choice(breakfast))
        bot.send_message(message.chat.id, answer, parse_mode = "MarkdownV2")
    elif message.text.strip() == 'Обеды' :
        answer = json_recipe_to_str(random.choice(lunch))
        bot.send_message(message.chat.id, answer, parse_mode = "MarkdownV2")
    elif message.text.strip() == 'Ужины':
        answer = json_recipe_to_str(random.choice(dinner))
        bot.send_message(message.chat.id, answer, parse_mode = "MarkdownV2")


bot.polling(none_stop=True, interval=0)
