from main import bot, dp, style_model, style_model_slow

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types.message import ContentType
from config import admin_id
from menu import menu, run_menu
from model import Net
from run import Run
from utils import *
from utils_slow import transfer_style_slow
import gc

async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text='Bot started')


@dp.message_handler(commands=['start'])
async def echo(message: Message):
    #await bot.send_message(chat_id=message.from_user.id, text=text)
    text = '''Добро пожаловать в Style Transfer Bot. 
Здесь ты можешь наложить на своё фото интересный фильтр. 
Для начала введи команду /run или нажми на соответствующую кнопку
Поехали!'''
    await message.answer(text=text, reply_markup=run_menu)

@dp.message_handler(commands=['help'])
async def help(message: Message):
    #await bot.send_message(chat_id=message.from_user.id, text=text)
    text = '''Здесь всё просто!
Нажми /start, чтобы начать работать с ботом.
Нажми /run, чтобы сделать еще одну крутую фотографию.
Нажми /info, чтобы узнать подробности о боте'''
    await message.answer(text=text)

@dp.message_handler(commands=['info'])
async def info(message: Message):
    #await bot.send_message(chat_id=message.from_user.id, text=text)
    text = '''Данный бот является демо-проектом, реализовнным в качестве проекта в школе dlschool.org'''
    await message.answer(text=text, reply_markup=run_menu)

@dp.message_handler(Command('run'), state=None)
@dp.message_handler(Text(equals=['Поехали']), state=None)
async def enter_run(message: Message): 
    await message.answer('Пришли мне любое фото, которое ты хочешь видоизменить.', reply_markup=ReplyKeyboardRemove())

    await Run.Img1.set()
    # или await Run.first()

@dp.message_handler(content_types=ContentType.PHOTO, state=Run.Img1)
async def get_photo_1(message: Message, state: FSMContext):
    path_content = f'content_{message.from_user.id}.jpg'
    await state.update_data(path_content=path_content)
    await message.photo[-1].download(path_content)
    await message.answer('А теперь у тебя два пути. Ты можешь выбрать один из предложенных стилей и получить готовый результат почти мгновенно, либо ты можешь загрузить свою картинку в качестве стиля, но придется подождать порядка 10 минут. Выбор за тобой!', reply_markup=menu)

    await Run.next()


@dp.message_handler(content_types=ContentType.PHOTO, state=Run.Img2)
@dp.message_handler(Text(equals=['wave', 'starry_night', 'mosaic', 'pencil', 'mosaic_ducks', 'candy', 'udnie', 'the_scream', 'strip', 'seated-nude', 'frida_kahlo', 'feathers']), state=Run.Img2)
async def get_photo_2(message: Message, state: FSMContext):
    
    data = await state.get_data()
    path_content = data.get('path_content')
    user_id = message.from_user.id

    if message.text is None:
        path_style = f'style_{message.from_user.id}.jpg'
        await message.photo[-1].download(path_style)
        await message.answer('Спасибо! Придется немного подождать. Можешь выходить из бота и заниматься своими делами. Когда будет готово, я пришлю результат!', reply_markup=ReplyKeyboardRemove())
        output_path = transfer_style_slow(path_content, path_style, style_model_slow, user_id)
    else:
        path_style = f'style/{message.text}.jpg'
        await message.answer('Спасибо! Сейчас будет результат', reply_markup=ReplyKeyboardRemove())
        output_path = transfer_style(path_content, path_style, style_model, user_id)

    photo = {'photo': open(output_path, 'rb')}
    await message.answer_photo(photo=photo['photo'])
    await message.answer('Готово!', reply_markup=run_menu)
    await state.reset_state()