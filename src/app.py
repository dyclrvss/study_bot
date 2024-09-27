from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from text import *
from dotenv import load_dotenv , find_dotenv
import os

find_dotenv() 
load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


class StartCommand:
    @dp.message_handler(commands=['start'])
    async def start_command(message: types.Message):
        await message.reply(greeting_text)

class HelpCommand:
    @dp.message_handler(commands = ['help'])
    async def help_command(message: types.Message):
        await message.reply(help_text)

class RandomImage:
    @dp.message_handler(commands=['randImg'])
    async def randImg_command(message: types.Message):
        await message.reply(randImg_text)

class RandomAudio:
    @dp.message_handler(commands=['randAudio'])
    async def randAudio_command(message: types.Message):
        await message.reply(randAudio_text)

class ImageByNum:
    @dp.message_handler(commands=['ImgByNum'])
    async def imgByNum_command(message: types.Message):
        await message.reply(f'{imgByNum_text} , 1')

class AudioBuNum:
    @dp.message_handler(commands=['AudioByNum'])
    async def audioByNum_command(message: types.Message):
        await message.reply(f'{audioByNum_text} , 1')

class UploadImage:
    @dp.message_handler(commands=['uploadImg'])
    async def uploadImg_command(message: types.Message):
        await message.reply(uploadImg_text)

class UploadAudio:
    @dp.message_handler(commands=['uploadAudio'])
    async def uploadAudio_command(message: types.Message):
        await message.reply(uploadAudio_text)

if __name__ == '__main__':
    executor.start_polling(dp)