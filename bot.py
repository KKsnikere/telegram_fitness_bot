import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

bot = telebot.TeleBot('5978521960:AAFGhXFNOTDpMUmn-J3nYSZ_7_TpXLJnz6c')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

button_bmi = KeyboardButton('BMI')
button_about = KeyboardButton('About')
keyboard.add(button_bmi, button_about)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello! Press the button to use bot funcions.', reply_markup=keyboard)

@bot.message_handler(commands=['about'])
def about(message):
    about_msg = "This Telegram bot is designed to help people stay fit and healthy by providing personalized workout plans and dietary advice.\nThe bot has several features, including a body mass index (BMI) calculator, also generates workout plans tailored to each user's fitness level, preferences, and goals, and recommends daily calorie intake based on their activity level, weight, and desired weight. It also offers helpful tips and advice on staying motivated and achieving fitness goals. With this bot, users can get all the support and guidance they need to lead a healthy lifestyle and stay in shape."
    bot.send_message(message.chat.id, about_msg)
    with open('about.gif', 'rb') as f:
        bot.send_animation(message.chat.id, f)

def calculate_bmi(weight, height):
    bmi = weight / (height/100)**2
    return bmi

def get_bmi_category(bmi):
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal weight"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"

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
    bmi_category = get_bmi_category(bmi)
    bot.send_message(message.chat.id, f'Your BMI: {bmi:.2f}\nCategory: {bmi_category}')

bot.polling(none_stop=True, interval=1)
