from main import bot, dp

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.types.message import ContentType
from config import admin_id
from menu import menu, run_menu
from run import Run
from utils import image_concat

async def send_to_admin(dp):
    await bot.send_message(chat_id=admin_id, text='Bot started')


@dp.message_handler(commands=['start'])
async def echo(message: Message):
    #await bot.send_message(chat_id=message.from_user.id, text=text)
    text = '''Добро пожаловать в Style Transfer Bot. 
Тебе необходимо по очереди прислать мне два фото. 
Для начала введи команду /run или нажми на соответствующую кнопку
Поехали!'''
    await message.answer(text=text, reply_markup=run_menu)

@dp.message_handler(Command('run'), state=None)
@dp.message_handler(Text(equals=['Поехали']), state=None)
async def enter_run(message: Message): 
    await message.answer('Пришли мне любое фото, которое ты хочешь видоизменить.', reply_markup=ReplyKeyboardRemove())

    await Run.Img1.set()
    # или await Run.first()

@dp.message_handler(content_types=ContentType.PHOTO, state=Run.Img1)
async def get_photo_1(message: Message, state: FSMContext):
    answer = '1'
    await state.update_data(answer1=answer)
    await message.photo[-1].download(f'img/content_{message.from_user.id}.jpg')
    await message.answer('А теперь я жду от тебя второе фото, которое ты хочешь использовать в качестве стиля, либо выбери из предложенных', reply_markup=menu)

    await Run.next()

@dp.message_handler(content_types=ContentType.PHOTO, state=Run.Img2)
@dp.message_handler(Text(equals=['Style1', 'Style2', 'Style3']), state=Run.Img2)
async def get_photo_2(message: Message, state: FSMContext):
    
    answer2 = message.text

    if message.text == 'Style1':
        path = 'style/style_1.jpg'
    elif message.text == 'Style2':
        path = 'style/style_2.jpg'
    elif message.text == 'Style3':
        path = 'style/style_3.jpg'
    elif message.text is None:
        await message.photo[-1].download(f'img/style_{message.from_user.id}.jpg')
        path = f'img/style_{message.from_user.id}.jpg'
    
    await message.answer('Спасибо! Ожидайте результат...', reply_markup=ReplyKeyboardRemove())

    data = await state.get_data()
    answer1 = data.get('answer1')
    #await message.photo[-1].download('img/style.jpg')
    

    await message.answer(f'{answer1} and {answer2}')

    image_concat(f'img/content_{message.from_user.id}.jpg', path)

    photo = {'photo': open('img/result.jpg', 'rb')}
    await message.answer_photo(photo=photo['photo'])
    
    #await state.finish()
    await state.reset_state()