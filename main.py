import telebot
from shared import TOKEN
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot(TOKEN)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

button_about = KeyboardButton('About')
button_test = KeyboardButton('Test')
keyboard.add(button_about, button_test)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello! Press the button to use bot functions.', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'About')
def about(message):
    about_msg = "This Telegram bot is designed to help people stay fit and healthy by providing personalized workout plans and dietary advice.\nThe bot has several features, including a body mass index (BMI) calculator, generates workout plans tailored to each user's fitness level, preferences, and goals, and recommends daily calorie intake based on their activity level, weight, and desired weight. It also offers helpful tips and advice on staying motivated and achieving fitness goals. With this bot, users can get all the support and guidance they need to lead a healthy lifestyle and stay in shape."
    bot.send_message(message.chat.id, about_msg)
    with open('gifs/about.gif', 'rb') as f:
        bot.send_animation(message.chat.id, f)


bot.polling(none_stop=True, interval=1)



