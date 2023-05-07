import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
from shared import TOKEN
from warmup import send_warmup_exercise

bot = telebot.TeleBot(TOKEN)

keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
training_button = KeyboardButton('Training')
keyboard.add(training_button)

@bot.message_handler(func=lambda message: message.text == 'Training')
def training_options(message):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
    warm_up_button = KeyboardButton('Warm-up')
    cardio_button = KeyboardButton('Cardio')
    strength_button = KeyboardButton('Strength')
    back_button = KeyboardButton('Back')
    keyboard.add(warm_up_button, cardio_button, strength_button, back_button)
    bot.send_message(message.chat.id, 'Choose your training type:', reply_markup=keyboard)

@bot.message_handler(func=lambda message: message.text == 'Warm-up')
def warmup_options(message):
    send_warmup_exercise(update=bot, context=message.chat.id)

bot.polling(none_stop=True, interval=1)