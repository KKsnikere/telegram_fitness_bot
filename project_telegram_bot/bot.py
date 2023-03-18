import time
import logging

from aiogram import Bot, Dispatcher, executor, types


TOKEN = "5978521960:AAFGhXFNOTDpMUmn-J3nYSZ_7_TpXLJnz6c"
MSG = "Did you code today?"

bot = Bot(token=TOKEN)
dp = Dispather(bot=bot)

@dp.message_handler(commands=['start'])
async def start_handler(message: type.Message):
    user_id = message.from_user.id
    user_name = message.from_user_full_name
    logging.info(f'{user_id=} {user_name=} {time.asctime()}')

    await message.reply(f"Hello,{user_name}")

    for i in range(10):
        time.sleep(60*60*24)
        await bot.send_message(user_id, MSG)

if __name__ == '__main__':
    executor.start_polling(dp)
