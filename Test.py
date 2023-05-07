import telebot, time
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from shared import TOKEN

bot = telebot.TeleBot(TOKEN)



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
        bot.register_next_step_handler(message, ask_height)
    else:
        bot.send_message(message.chat.id, 'Please select your gender from the options provided.')
        bot.register_next_step_handler(message, ask_age)

def ask_height(message):
    user_data['age'] = float(message.text)
    bot.send_message(message.chat.id, 'Enter your height (cm):')
    bot.register_next_step_handler(message, ask_weight)

def ask_weight(message):
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
    bot.register_next_step_handler(message, handle_activity)


def handle_activity(message):
    user_data['activity_level'] = message.text

    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(KeyboardButton(text='Lose weight'))
    keyboard.add(KeyboardButton(text='Maintain weight'))
    keyboard.add(KeyboardButton(text='Gain weight'))
    keyboard.add(KeyboardButton(text='Calculate BMI'))

    bot.send_message(message.chat.id, 'What is your goal?', reply_markup=keyboard)
    bot.register_next_step_handler(message, handle_goal)


def handle_goal(message):
    if 'goal' not in user_data:
        if message.text in ['Lose weight', 'Maintain weight', 'Gain weight', 'Calculate BMI']:
            user_data['goal'] = message.text
            if message.text == 'Calculate BMI':
                bmi = calculate_bmi(user_data['weight'], user_data['height'])
                bmi_category = get_bmi_category(bmi)
                bot.send_message(message.chat.id, f'Your BMI: {bmi:.2f}\nCategory: {bmi_category}')

            else:

                bmr = calculate_bmr(user_data['gender'], user_data['weight'], user_data['height'], user_data['age'])
                tdee = calculate_tdee(bmr, user_data['activity_level'])
                calories = calculate_calories(tdee, user_data['goal'])
                macros = calculate_macros(calories)

                bot.send_message(message.chat.id, f'Your daily caloric needs are: {calories:.0f} calories', reply_markup=ReplyKeyboardRemove())
                bot.send_message(message.chat.id, f'Your daily macronutrient needs are:\nProtein: {macros["protein"]:.0f} g\nFat: {macros["fat"]:.0f} g\nCarbohydrates: {macros["carbs"]:.0f} g', reply_markup=ReplyKeyboardRemove())
                bot.send_message(message.chat.id, 'Test completed')
           
           
    else:
        bot.send_message(message.chat.id, 'Thank you for using this bot!')

def calculate_bmi(weight, height):
    bmi = weight / (height / 100) ** 2
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



def calculate_macros(calories):
    protein = calories * 0.33 / 4
    fat = calories * 0.33 / 9
    carbs = (calories - protein * 4 - fat * 9) / 4
    return {'protein': protein, 'fat': fat, 'carbs': carbs}
    
def calculate_bmr(gender, weight, height, age):
    if gender == 'Male':
        bmr = 88.362 + (13.397 * weight) + (4.799 * height) - (5.677 * age)
    elif gender == 'Female':
        bmr = 447.593 + (9.247 * weight) + (3.098 * height) - (4.330 * age)
    else:
        raise ValueError("Invalid gender")
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