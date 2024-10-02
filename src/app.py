from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from text import *   
from db_select import *  
from db_upload import *
from dotenv import load_dotenv, find_dotenv
import os
from aiogram.dispatcher import FSMContext
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import InputFile , ChatActions
from datetime import datetime

find_dotenv()
load_dotenv()
TOKEN = os.getenv('TOKEN')

storage = MemoryStorage()
bot = Bot(token=TOKEN)
dp = Dispatcher(bot , storage= storage)
class Form(StatesGroup):
    imgNum = State()
    audioNum = State()
    image = State()
    audio = State()

@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply(greeting_text % message.from_user.first_name)

@dp.message_handler(commands=['help'])
async def help_command(message: types.Message):
    await message.reply(help_text)

@dp.message_handler(commands=['randImg'])
async def randImg_command(message: types.Message):
    try:
        await message.reply(randImg_text)
        await message.reply("Please wait a moment...")
        await bot.send_chat_action(message.chat.id, ChatActions.UPLOAD_PHOTO)
        await sendRandImg(message)
    except Exception as e:
        print(f"Error in randImg_command: {e}")

async def sendRandImg(message: types.Message):
    try:
        img_path = FileSelect.select_random_file("image")
        img = InputFile(os.path.join(os.curdir, 'locale', 'images', img_path))
        await message.answer_photo(img)
    except Exception as e:
        print(e)

@dp.message_handler(commands=['randAudio'])
async def randAudio_command(message: types.Message):
    try:
        await message.reply(randAudio_text)
        await message.reply("Please wait a moment...")
        await bot.send_chat_action(message.chat.id, ChatActions.UPLOAD_AUDIO)
        await sendRandAudio(message)
    except Exception as e:
        print(e)

async def sendRandAudio(message: types.Message):
    try:
        audio_path = FileSelect.select_random_file("audio")
        audio = InputFile(os.path.join(os.curdir, 'locale', 'audios', audio_path))
        await message.answer_audio(audio)
    except Exception as e:
        print(e)


@dp.message_handler(commands=['ImgByNum'])
async def imgByNum_command(message: types.Message):
    try:
        num = FileSelect.select_max_id("image")
        await message.reply(f'{imgByNum_text} ( 1 , {num} )')
        await Form.imgNum.set()
        async with dp.current_state(user=message.from_user.id).proxy() as data:
            data['max_num'] = num
    except Exception as e:
        print(e)

@dp.message_handler(state=Form.imgNum)
async def sendImgByNum(message: types.Message, state: FSMContext):
    try:
        if not message.text.isdigit():
            await message.reply("Please, send an integer.")
            return
        number = int(message.text)
        async with state.proxy() as data:
            max_num = data['max_num']
        if number > max_num or number < 1:
            await message.reply(f"Please enter a number between 1 and {max_num}.")
            return
        img_path = FileSelect.file_select("image", number)
        img = InputFile(os.path.join(os.curdir, 'locale', 'images', img_path))
        await message.reply("Please wait a moment...")
        await bot.send_chat_action(message.chat.id, ChatActions.UPLOAD_PHOTO)
        await message.answer_photo(img)
        await state.finish()
    except Exception as e:
        print(e)


@dp.message_handler(commands=['AudioByNum'])
async def audioByNum_command(message: types.Message):
    try:
        num = FileSelect.select_max_id("audio")
        await message.reply(f'{audioByNum_text} ( 1 , {num} )')
        await Form.audioNum.set()
        async with dp.current_state(user=message.from_user.id).proxy() as data:
            data['max_num'] = num
    except Exception as e:
        print(e)

@dp.message_handler(state=Form.audioNum)
async def sendAudioByNum(message: types.Message, state: FSMContext):
    try:
        if not message.text.isdigit():
            await message.reply("Please, send an integer.")
            return
        number = int(message.text)
        async with state.proxy() as data:
            max_num = data['max_num']
        if number > max_num or number < 1:
            await message.reply(f"Please enter a number between 1 and {max_num}.")
            return
        audio_path = FileSelect.file_select("audio", number)
        audio = InputFile(os.path.join(os.curdir, 'locale', 'audios', audio_path))
        await message.reply("Please wait a moment...")
        await bot.send_chat_action(message.chat.id, ChatActions.UPLOAD_AUDIO)
        await message.answer_audio(audio)
        await state.finish()
    except Exception as e:
        print(e)

@dp.message_handler(commands=['uploadImg'])
async def uploadImg_command(message: types.Message):
    try:
        await message.reply(uploadImg_text)
        await Form.image.set()
    except Exception as e:
        print(e)

@dp.message_handler(state=Form.image, content_types=types.ContentType.PHOTO)
async def uploadImage(message: types.Message, state: FSMContext):
    try:
        if not message.photo:
            await message.answer("Please, send an image in PNG/GIF/JPG format")
            return
        img = message.photo[-1].file_id
        img_info = await bot.get_file(img)
        img_name = f"photo_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.jpg"
        await message.answer("Image recieved!")
        destination = os.path.join(os.curdir, 'locale', 'images', img_name)
        await bot.download_file(img_info.file_path, destination)
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        imgId = FileUpload.uploadFile("image", img_name) 
        await message.answer(f"Image id is: {imgId}")  
        await state.finish()  
    except Exception as e:
        print(e)
        await message.answer("An error occurred while processing the image.")

@dp.message_handler(commands=['uploadAudio'])
async def uploadAudio_command(message: types.Message):
    try:
        await message.reply(uploadAudio_text)
        await Form.audio.set()
    except Exception as e:
        print(e)

@dp.message_handler(state=Form.audio, content_types=types.ContentType.AUDIO)
async def uploadAudio(message: types.Message, state: FSMContext):
    try:
        if not message.audio:
            await message.answer("Please, send an audio in MP3 format")
            return
        await message.answer("Audio recieved!")
        audio = message.audio.file_id
        audio_info = await bot.get_file(audio)
        audio_name = message.audio.file_name if message.audio.file_name else f"audio_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.mp3"
        destination = os.path.join(os.curdir, 'locale', 'audios', audio_name)
        await bot.download_file(audio_info.file_path, destination)
        await bot.send_chat_action(message.chat.id, ChatActions.TYPING)
        audioId = FileUpload.uploadFile("audio", audio_name) 
        await message.answer(f"Audio id is: {audioId}")  
        await state.finish()  
    except Exception as e:
        print(e)
        await message.answer("An error occurred while processing the audio.")

if __name__ == '__main__':
    executor.start_polling(dp)