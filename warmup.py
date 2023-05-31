import sqlite3
import random
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


def send_warmup_exercise(update, context):
    conn = sqlite3.connect('trains.db')
    cursor = conn.cursor()

    cursor.execute('SELECT name, description, gif_path FROM warmups ORDER BY RANDOM() LIMIT 1')
    result = cursor.fetchone()
    if result:
        exercise_name, exercise_description, exercise_gif = result
    else:
        return

    message_text = "Warmup:\n{}\n\nFirst exercise:\n{}".format(exercise_description, exercise_name)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)

    context.bot.send_animation(chat_id=update.effective_chat.id, animation=exercise_gif)

    keyboard = [[InlineKeyboardButton("Second exercise", callback_data='next_warmup_exercise')],
                [InlineKeyboardButton("Exit", callback_data='exit_warmup')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=update.effective_chat.id, text="Choose an action:", reply_markup=reply_markup)

    cursor.close()
    conn.close()

def next_warmup_exercise(update, context):
    conn = sqlite3.connect('trains.db')
    cursor = conn.cursor()

    cursor.execute('SELECT name, gif_path FROM warmups ORDER BY RANDOM() LIMIT 1')
    result = cursor.fetchone()
    exercise_name, exercise_gif = result

    context.bot.send_message(chat_id=update.effective_chat.id, text=exercise_name)
    context.bot.send_animation(chat_id=update.effective_chat.id, animation=exercise_gif)

    keyboard = [[InlineKeyboardButton("Next exercise", callback_data='next_warmup_exercise')],
            [InlineKeyboardButton("Exit to menu", callback_data='exit_warmup')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(chat_id=update.effective_chat.id, text="Choose an action:", reply_markup=reply_markup)

    cursor.close()
    conn.close()
