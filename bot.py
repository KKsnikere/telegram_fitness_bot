import telebot
bot = telebot.TeleBot('5978521960:AAFGhXFNOTDpMUmn-J3nYSZ_7_TpXLJnz6c')

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello')

@bot.message_handler(commands=['about'])
def about(message):
    about_msg="This Telegram bot is designed to help people stay fit and healthy by providing personalized workout plans and dietary advice.\nThe bot has several features, including a body mass index (BMI) calculator, also generates workout plans tailored to each user's fitness level, preferences, and goals, and recommends daily calorie intake based on their activity level, weight, and desired weight. It also offers helpful tips and advice on staying motivated and achieving fitness goals. With this bot, users can get all the support and guidance they need to lead a healthy lifestyle and stay in shape."
    bot.send_message(message.chat.id, about_msg)

@bot.message_handler(commands=['help'])
def bmi(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    bmi = types.KeyboardButton('BMI')

    markup.add(bmi)
    bot.send_message(message.chat.id, 'Help', reply_markup=markup)




bot.polling(none_stop=True, interval=1)

