import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot('5978521960:AAFGhXFNOTDpMUmn-J3nYSZ_7_TpXLJnz6c')


keyboard = ReplyKeyboardMarkup(resize_keyboard=True)


button_bmi = KeyboardButton('BMI')
button_about = KeyboardButton('About')


keyboard.add(button_bmi, button_about)


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello! Press the button to calculate BMI.', reply_markup=keyboard)


@bot.message_handler(commands=['about'])
def about(message):
    about_msg = "This is a Telegram bot designed to help people stay fit and healthy by providing personalized workout plans and dietary advice."
    bot.send_message(message.chat.id, about_msg)

def calculate_bmi(weight, height):
    bmi = weight / (height/100)**2
    return bmi


@bot.message_handler(func=lambda message: True)
def handle_keyboard(message):
    if message.text == 'BMI':
        bot.send_message(message.chat.id, 'Enter your weight(kg):')
        bot.register_next_step_handler(message, ask_height)
    elif message.text == 'About':
        about(message)

def ask_height(message):
    weight = float(message.text)
    bot.send_message(message.chat.id, 'Enter your height(cm):')
    bot.register_next_step_handler(message, show_bmi, weight)

def show_bmi(message, weight):
    height = float(message.text)
    bmi = calculate_bmi(weight, height)
    bot.send_message(message.chat.id, f'Your BMI: {bmi:.2f}')

bot.polling(none_stop=True, interval=1)
