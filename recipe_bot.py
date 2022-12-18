import telebot
from telebot import types
import random
import json
import sqlite3
token="5371708856:AAFjSjtyderlCBeg05W2K1FKXNAVLEQaDKg"
bot=telebot.TeleBot(token)
eat = {}  
state = {}
temp = {}

def escape_chars(line):
    return line.replace("(", r"\(").replace(")", r"\)").replace(".", r"\.").replace("-", r"\-")
    
def recipe_to_str(recipe, ingredients):
    L = []
    for i in range(len(ingredients)):
        ingredient_trans = f'{ingredients[i][0]} - {ingredients[i][1]} {ingredients[i][2]}'
        L.append(ingredient_trans)
        
 
    text = ";\n".join(L) + '.'
    
    
    main_template = f'''{recipe[1]}
        
{text}

{recipe[2]}'''
    
    
    

    return escape_chars(main_template)
    
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

def get_answer(eating, temperature, vegateriancy):
    con = sqlite3.connect("New_recipes_base.db")
    cur = con.cursor()
    if vegateriancy == 'Vegan':
        veg = 'true'
    elif vegateriancy == 'NotVegan':
        veg = 'false'
    elif vegateriancy == 'Неважно':
        veg = 'recipes.vegan'
    else:
        raise ValueError('unexpected value of vegateriancy, possible values: "Vegan", "NotVegan". Received value - "{vegateriancy}"')
        
    if eating == 'Завтраки':
        e = 0
    elif eating == 'Обеды':
        e = 1
    elif eating == 'Ужины':
        e = 2
    elif eating == 'Неважно':
        e = 'recipes_eating.id_eating'
    else:
        raise ValueError(f'unexpected value of eating, possible values: "Завтраки", "Обеды", "Ужины", "Неважно". Received value - "{eating}"')
        
    if temperature == 'hot':
        temper = "'hot'"
    elif temperature == 'cold':
        temper = "'cold'"
    elif temperature == 'Неважно':
        temper = 'recipes.temperature'
    else:
        raise ValueError(f'unexpected value of temperature, possible values: "hot", "cold". Received value -"{temperature}"')
        
    #if temperature == 'Неважно' and eating == 'Неважно' and vegateriancy == 'Неважно':
        
        
    sql_template1 = f"""select id_recipe, name, cooking 
                      from recipes 
                      join recipes_eating on recipes_eating.id_recipe = recipes.id 
                      where recipes.temperature = {temper}
                            and recipes.vegan = {veg}
                            and recipes_eating.id_eating = {e} 
                      order by random() 
                      limit 1 """
    
    print(sql_template1)
    res = cur.execute(sql_template1)    
    recipe = res.fetchone()
    if recipe is None:
        return escape_chars(f'Рецепта по заданным критериям нет. Received value - "{temperature}", "{eating}", "{vegateriancy}"')
    
    
    sql_template2 = """ select i.name, ri.amount, u.name 
                        from ingredients as i 
                        join recipes_ingredients as ri on ri.id_ingredient = i.id 
                        join unit as u on u.id = i.id_unit
                        where id_recipe = {id_recipe};
    """
    res = cur.execute(sql_template2.format(id_recipe = recipe[0]))    
    ingredients = res.fetchall()
    
    #return str(r1).replace("(", r"\(").replace(")", r"\)").replace(".", r"\.") + str(r2).replace("(", r"\(").replace(")", r"\)").replace(".", r"\.")
     
    return recipe_to_str(recipe, ingredients)
 

     
@bot.message_handler(content_types=["text"])
def handle_text(message):
    global eat
    global state
    global temp
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

        answer = get_answer(eat[message.chat.id], temp[message.chat.id], text)
        
        bot.send_message(message.chat.id, answer, parse_mode = "MarkdownV2",  reply_markup=markup)
        state[message.chat.id] = 0 
        
    else:
        bot.send_message(message.chat.id, 'Я тупой и не понимаю сложных слов, нажимайте кнопки пожалуйста. ')
        markup = get_markup(["Рецепт"])
        bot.send_message(message.chat.id, 'Нажми: \nРецепт для получения рецепт ',  reply_markup=markup)
        [message.chat.id] == 0
        
bot.polling(none_stop=True, interval=0)
