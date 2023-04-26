import telebot, time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

bot = telebot.TeleBot('5978521960:AAFGhXFNOTDpMUmn-J3nYSZ_7_TpXLJnz6c')
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)

button_bmi = KeyboardButton('BMI')
button_about = KeyboardButton('About')
button_test = KeyboardButton('Test')
keyboard.add(button_bmi, button_about, button_test)

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
    elif message.text == 'Test':
        test(message)
        bot.register_next_step_handler(message, handle_message)

        
def ask_height(message):
    weight = float(message.text)
    bot.send_message(message.chat.id, 'Enter your height(cm):')
    bot.register_next_step_handler(message, show_bmi, weight)


def show_bmi(message, weight):
    height = float(message.text)
    bmi = calculate_bmi(weight, height)
    bmi_category = get_bmi_category(bmi)
    bot.send_message(message.chat.id, f'Your BMI: {bmi:.2f}\nCategory: {bmi_category}')






#test for daily calorie needs

user_data = {}

@bot.message_handler(commands=['Test'])
def test(message):
    
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Male'))
    keyboard.add(KeyboardButton(text='Female'))

    bot.send_message(message.chat.id, 'What is your gender?', reply_markup=keyboard)
    bot.register_next_step_handler(message, ask_age)

def ask_age(message):
    if message.text == 'Male' or message.text == 'Female':
        user_data['gender'] = message.text
        bot.send_message(message.chat.id, 'Enter your age:')
        bot.register_next_step_handler(message, ask_height2)
    else:
        bot.send_message(message.chat.id, 'Please select your gender from the options provided.')
        bot.register_next_step_handler(message, ask_age)

def ask_height2(message):
    user_data['age'] = float(message.text)
    bot.send_message(message.chat.id, 'Enter your height (cm):')
    bot.register_next_step_handler(message, ask_weight2)

def ask_weight2(message):
    user_data['height'] = float(message.text)
    bot.send_message(message.chat.id, 'Enter your weight (kg):')
    bot.register_next_step_handler(message, ask_activity)

def ask_activity(message):
    user_data['weight'] = float(message.text)
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Sedentary (little or no exercise)'))
    keyboard.add(KeyboardButton(text='Lightly active (light exercise or sports 1-3 days a week)'))
    keyboard.add(KeyboardButton(text='Moderately active (moderate exercise or sports 3-5 days a week)'))
    keyboard.add(KeyboardButton(text='Very active (hard exercise or sports 6-7 days a week)'))
    keyboard.add(KeyboardButton(text='Super active (very hard exercise or sports, physical job or training twice a day)'))

    bot.send_message(message.chat.id, 'Select your activity level:', reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_message)

def handle_message(message):
    user_data['activity_level'] = message.text

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Lose weight'))
    keyboard.add(KeyboardButton(text='Maintain weight'))
    keyboard.add(KeyboardButton(text='Gain weight'))

    bot.send_message(message.chat.id, 'What is your goal?', reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_message3)


def handle_message3(message):
    if 'goal' not in user_data:
        if message.text in ['Lose weight', 'Maintain weight', 'Gain weight']:
            user_data['goal'] = message.text

            bmr = calculate_bmr(user_data['gender'], user_data['weight'], user_data['height'], user_data['age'])
            tdee = calculate_tdee(bmr, user_data['activity_level'])
            calories = calculate_calories(tdee, user_data['goal'])
            macros = calculate_macros(calories)

            bot.send_message(message.chat.id, f'Your daily caloric needs are: {calories:.0f} calories', reply_markup=ReplyKeyboardRemove())
            bot.send_message(message.chat.id, f'Your daily macronutrient needs are:\nProtein: {macros["protein"]:.0f} g\nFat: {macros["fat"]:.0f} g\nCarbohydrates: {macros["carbs"]:.0f} g', reply_markup=ReplyKeyboardRemove())
            bot.send_message(message.chat.id, 'Test completed')
           
           
    else:
        bot.send_message(message.chat.id, 'Thank you for using this bot!')

def calculate_macros(calories):
    protein = calories * 0.33 / 4
    fat = calories * 0.33 / 9
    carbs = (calories - protein * 4 - fat * 9) / 4
    return {'protein': protein, 'fat': fat, 'carbs': carbs}
    
def calculate_bmr(gender, weight, height, age):
    if gender == 'Male':
        bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
    else:
        bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)
    return bmr


def calculate_tdee(bmr, activity_level):
    if activity_level == 'Sedentary (little or no exercise)':
        tdee = bmr * 1.2
    elif activity_level == 'Lightly active (light exercise or sports 1-3 days a week)':
        tdee = bmr * 1.375
    elif activity_level == 'Moderately active (moderate exercise or sports 3-5 days a week)':
        tdee = bmr * 1.55
    elif activity_level == 'Very active (hard exercise or sports 6-7 days a week)':
        tdee = bmr * 1.725
    else:
        tdee = bmr * 1.9
    return tdee


def calculate_calories(tdee, goal):
    if goal == 'Lose weight':
        calories = tdee*0.8
    elif goal == 'Maintain weight':
        calories = tdee
    else:
        calories = tdee*1.2
    return calories


bot.polling(none_stop=True, interval=1)

