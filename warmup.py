import sqlite3
import random
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup


# Создаем функцию для отправки пользователю упражнения и описания разминки
def send_warmup_exercise(update, context):

    # Подключаемся к базе данных с упражнениями для разминки
    conn = sqlite3.connect('trains.db')
    cursor = conn.cursor()

    # Выбираем случайное упражнение из базы данных
    cursor.execute('SELECT name, description, gif_path FROM warmups ORDER BY RANDOM() LIMIT 1')
    result = cursor.fetchone()
    exercise_name, exercise_description, exercise_gif = result

    # Отправляем пользователю описание разминки и первое упражнение
    message_text = "Для чего нужна разминка:\n{}\n\nПервое упражнение:\n{}".format(exercise_description, exercise_name)
    context.bot.send_message(chat_id=update.effective_chat.id, text=message_text)

    # Отправляем пользователю гифку с упражнением
    context.bot.send_animation(chat_id=update.effective_chat.id, animation=exercise_gif)

    # Создаем кнопки "Следующее упражнение" и "Выход в меню"
    keyboard = [[InlineKeyboardButton("Следующее упражнение", callback_data='next_warmup_exercise')],
                [InlineKeyboardButton("Выход в меню", callback_data='exit_warmup')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем кнопки пользователю
    context.bot.send_message(chat_id=update.effective_chat.id, text="Выберите действие:", reply_markup=reply_markup)

    cursor.close()
    conn.close()

# Обрабатываем нажатие на кнопку "Следующее упражнение"
def next_warmup_exercise(update, context):
    # Выбираем следующее случайное упражнение из базы данных
    cursor.execute('SELECT name, gif_path FROM warmups ORDER BY RANDOM() LIMIT 1')
    result = cursor.fetchone()
    exercise_name, exercise_gif = result

    # Отправляем пользователю следующее упражнение
    context.bot.send_message(chat_id=update.effective_chat.id, text=exercise_name)
    context.bot.send_animation(chat_id=update.effective_chat.id, animation=exercise_gif)

    # Обновляем кнопки для управления процессом разминки
    keyboard = [[InlineKeyboardButton("Next exercise", callback_data='next_warmup_exercise')],
            [InlineKeyboardButton("Exit to menu", callback_data='exit_warmup')]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Отправляем кнопки пользователю
    context.bot.send_message(chat_id=update.effective_chat.id, text="Choose an action:", reply_markup=reply_markup)
