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
temp = {}

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
    photo = bot.send_photo(m.chat.id, "AgACAgIAAxkDAAIDqWMosr6BmAAB3FfTypauUlzGTepkKwACLL8xG6wxaEhG7i4VDcBVJwEAAwIAA3gAAykE", 'Нажми: \nРецепт для получения рецепт ',  reply_markup=markup)
    state[m.chat.id] = 0


@bot.message_handler(content_types=["text"])
def handle_text(message):
    global eat
    global state
    text = message.text.strip()
    
    if text == 'Рецепт' and state.get(message.chat.id, 0) == 0:
        markup = get_markup(["Завтраки", "Обеды", "Ужины", "Неважно"])
        bot.send_message(message.chat.id, 'Нажми: \nНа какой прием пищи вы хотите получить рецепт? ',  reply_markup=markup)
        state[message.chat.id] = 1
        
    elif text in ['Завтраки', 'Обеды', 'Ужины', "Неважно"] and state[message.chat.id] == 1 :
        eat[message.chat.id] = text
        
        markup = get_markup(["cold", "hot", "Неважно"])
        bot.send_message(message.chat.id, 'Нажми: \nКакой температуры вы бы хотели блюдо? ',  reply_markup=markup)
        
        state[message.chat.id] = 2
        
    elif text in ['cold', 'hot', "Неважно"] and state[message.chat.id] == 2:
        markup = get_markup(["Vegan", "NotVegan", "Неважно"])
        temp[message.chat.id] = text
        bot.send_message(message.chat.id, 'Нажми: \nВы бы хотели вегетерианское блюдо или нет? ',  reply_markup=markup)
        state[message.chat.id] = 3
        
    elif text in ['Vegan', 'NotVegan', "Неважно"] and state[message.chat.id] == 3:
        markup = get_markup(["Рецепт"])
        
        L = []
        K = []
        J = []
        
        if eat[message.chat.id] == "Неважно":
            L = recipes
        else:
            for i in range(len(recipes)):
                if eat[message.chat.id] in recipes[i]["eating"]:
                    L.append(recipes[i])           
        if temp[message.chat.id] == "Неважно":
            K = L
        else:
            for i in range(len(L)):        
                if temp[message.chat.id] in L[i]["temperature"]:
                    K.append(L[i])            
        if text  == "Неважно":
            J = K

        else:
            for i in range(len(K)):        
                if (text == "Vegan") == K[i]["vegaterian"]:
                    J.append(K[i])      
        if J == []:
            answer = "Блюдо с данными параметрами не найдено"
        else:
            Q = random.choice(J)
            print(Q)
            answer = json_recipe_to_str(Q)
                
                

        bot.send_message(message.chat.id, answer, parse_mode = "MarkdownV2",  reply_markup=markup)
        state[message.chat.id] = 0 
        
    else:
        bot.send_message(message.chat.id, 'Я тупой и не понимаю сложных слов, нажимайте кнопки пожалуйста. ')
        markup = get_markup(["Рецепт"])
        bot.send_message(message.chat.id, 'Нажми: \nРецепт для получения рецепт ',  reply_markup=markup)
        [message.chat.id] == 0
        
bot.polling(none_stop=True, interval=0)
