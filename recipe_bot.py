import telebot
from telebot import types
import random
import json
token="5371708856:AAFjSjtyderlCBeg05W2K1FKXNAVLEQaDKg"
bot=telebot.TeleBot(token)
f = open('recipes.json', 'r', encoding='UTF-8')
recipes = json.load(f)
f.close()
eat = {}  
state = {}

def json_recipe_to_str(r):
    return f'*Блюдо:* {r["name"]}.\n*Состав:* {", ".join(r["ingredients"])}.\n*Алгоритм Приготовления:* {r["recipe"]}'.replace(".", "\.")
    
def get_markup(names):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    for name in names:
        item=types.KeyboardButton(name)
        markup.add(item)
    return markup

@bot.message_handler(commands=["start"])
def start(m, res=False):
    global state
    markup = get_markup(["Рецепт"])
    bot.send_message(m.chat.id, 'Нажми: \nРецепт для получения рецепт ',  reply_markup=markup)
    state[m.chat.id] = 0


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global eat
    global state
    print(eat)
    if message.text.strip() == 'Рецепт' and state[message.chat.id] == 0:
        markup = get_markup(["Завтраки", "Обеды", "Ужины"])
        bot.send_message(message.chat.id, 'Нажми: \nНа какой прием пищи вы хотите получить рецепт? ',  reply_markup=markup)
        state[message.chat.id] = 1
        
    elif message.text.strip() == 'Завтраки' or message.text.strip() == 'Обеды' or message.text.strip() == 'Ужины' and [message.chat.id] == 1 :
        markup = get_markup(["cold", "hot"])
        eat[message.chat.id] = message.text.strip()
        bot.send_message(message.chat.id, 'Нажми: \nКакой температуры вы бы хотели блюдо? ',  reply_markup=markup)
        [message.chat.id] == 2
        
    elif  message.text.strip() == 'cold' or message.text.strip() == 'hot'  and [message.chat.id] == 2:
        markup = get_markup(["Рецепт"])
        L = []
        for i in range(len(recipes)):
            if eat[message.chat.id] in recipes[i]["eating"] and  message.text.strip() == recipes[i]["temperature"]:
                L.append(recipes[i])
        answer = json_recipe_to_str(random.choice(L))
        bot.send_message(message.chat.id, answer, parse_mode = "MarkdownV2",  reply_markup=markup)
        [message.chat.id] == 3
        
    else:
        bot.send_message(message.chat.id, 'Я тупой и не понимаю сложных слов, нажимайте кнопки пожалуйста. ')
        markup = get_markup(["Рецепт"])
        bot.send_message(message.chat.id, 'Нажми: \nРецепт для получения рецепт ',  reply_markup=markup)
        [message.chat.id] == 0
        
bot.polling(none_stop=True, interval=0)
