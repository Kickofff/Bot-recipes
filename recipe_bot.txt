import telebot
token="5371708856:AAFjSjtyderlCBeg05W2K1FKXNAVLEQaDKg"
"bot=telebot.Telebot(5371708856:AAFjSjtyderlCBeg05W2K1FKXNAVLEQaDKg)
f = open('/d/занятия_прог/bot-recipes/recipe.txt', 'r', encoding='UTF-8')
jokes = f.read().split('\n')
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
            answer = random.choice(facts)
	bot.send_message(message.chat.id, answer)
bot.polling(none_stop=True, interval=0)
