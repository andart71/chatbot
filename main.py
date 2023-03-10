import os
import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

openai.api_key = ""
API_TOKEN_BOT = '6093342208:AAFxPFdWCF89rJWLzOLBiWAcOwmdJCOZB7k'

bot = Bot(token=API_TOKEN_BOT)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())


class Form(StatesGroup):
    context_user = State({})


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! О чем поболтаем??")


@dp.message_handler(commands=['talking'])
async def send_welcome(message: types.Message, state: FSMContext):

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text(),
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6
    )
    await message.reply(response.choices[0].text)


@dp.message_handler()
async def send_letsgo(message: types.Message, state: FSMContext):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=message.text(),
        temperature=0.9,
        max_tokens=1000,
        top_p=1,
        frequency_penalty=0.0,
        presence_penalty=0.6
    )
    await message.reply(response.choices[0].text)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
