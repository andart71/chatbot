import os
import openai
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher import FSMContext

openai.api_key = "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"
API_TOKEN_BOT = '6093342208:AAHCBlKnqV3FCh5aJZMBkP3hEdwg4I3GoVc'


bot = Bot(token=API_TOKEN_BOT)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=MemoryStorage())

class Form(StatesGroup):
    context_user = State({})


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):

        await message.reply("Привет! О чем поболтаем??")

@dp.message_handler(commands=['talking'])
async def send_welcome(message: types.Message,  state:FSMContext):
    new_context_user = {}
    async with state.proxy() as data:
        print(data)
        context_user = data
        message_id_string = str(message.from_id)
        if message.from_id in context_user:
            print("OLD")
            new_context_user[message_id_string] = f"{context_user[message_id_string]} {message.text}\n"
        else:
            print("NEW")
            new_context_user[message_id_string] = f"{message.text}\n"

    print(new_context_user)
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=new_context_user[message_id_string],
        temperature=0,
        max_tokens=1000,
        top_p=1.0,
        frequency_penalty=0.5,
        presence_penalty=0.0
    )
    new_context_user[message_id_string] = f"{new_context_user[message_id_string]} {response.choices[0].text}\n"
    async with state.proxy() as data:
        data = new_context_user
    print(new_context_user)
    await message.reply(response.choices[0].text)

@dp.message_handler()
async def send_letsgo(message: types.Message, state:FSMContext):
        new_context_user = {}
        async with state.proxy() as data:
            print(data)
            context_user = data
            message_id_string = str(message.from_id)
            if message.from_id in context_user:
                print("OLD")
                new_context_user[message_id_string] = f"{context_user[message_id_string]} {message.text}\n"
            else:
                print("NEW")
                new_context_user[message_id_string] = f"{message.text}\n"

        print(new_context_user)
        response = openai.Completion.create(
          model="text-davinci-003",
          prompt=new_context_user[message_id_string],
          temperature=0,
          max_tokens=1000,
          top_p=1.0,
          frequency_penalty=0.5,
          presence_penalty=0.0
        )
        new_context_user[message_id_string] = f"{new_context_user[message_id_string]} {response.choices[0].text}\n"
        async with state.proxy() as data:
            data = new_context_user
        print(new_context_user)
        await message.reply(response.choices[0].text)

if __name__ == '__main__':
   executor.start_polling(dp, skip_updates=True)