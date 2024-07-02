import openai
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

API_TOKEN = '7298316359:AAHYkti5BXc6PA5kOjpuvJbl6pO8w1SMBUQ'
openai.api_key = '02.09.23'
openai.api_base = "https://arty-ai.onrender.com/v1"

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

context = []

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот на основе ChatGPT. Задай мне вопрос!")

@dp.message_handler()
async def handle_message(message: types.Message):
    global context
    user_message = message.text
    
    context.append(
        {"role": "system", "content": "Ты чат-бот ForgetGPT, "
                                      "Твоя модель - GPT3.5 Turbo, "
                                      "Отвечай по-русски. "})
    context.append({"role": "user", "content": message.text})

    try:
        response = openai.ChatCompletion.create(
            stream=False,
            model="gpt-3.5-turbo-16k",
            messages=context,
        )

        bot_response = response['choices'][0]['message']['content'].strip()

        context.append({"role": "assistant", "content": bot_response})

        await message.reply(bot_response, parse_mode=ParseMode.MARKDOWN)

    except Exception as e:
        error_message = f"Произошла ошибка: {str(e)}"

        await message.reply(error_message)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
