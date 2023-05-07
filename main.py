from shared import TOKEN
print(TOKEN)
import telebot, time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from Test import test


bot = telebot.TeleBot(TOKEN)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)


button_about = KeyboardButton('About')
button_test = KeyboardButton('Test')
keyboard.add(button_about, button_test)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello! Press the button to use bot funcions.', reply_markup=keyboard)

@bot.message_handler(commands=['about'])
def about(message):
    about_msg = "This Telegram bot is designed to help people stay fit and healthy by providing personalized workout plans and dietary advice.\nThe bot has several features, including a body mass index (BMI) calculator, also generates workout plans tailored to each user's fitness level, preferences, and goals, and recommends daily calorie intake based on their activity level, weight, and desired weight. It also offers helpful tips and advice on staying motivated and achieving fitness goals. With this bot, users can get all the support and guidance they need to lead a healthy lifestyle and stay in shape."
    bot.send_message(message.chat.id, about_msg)
    with open('gifs/about.gif', 'rb') as f:
        bot.send_animation(message.chat.id, f)


@bot.message_handler(func=lambda message: True)
def handle_keyboard(message):
   
    if message.text == 'About':
        about(message)
    if message.text == 'Test':
        test(message)




bot.polling(none_stop=True, interval=1)

