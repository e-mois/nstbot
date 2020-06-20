from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

run_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Поехали')
        ]
    ],
    resize_keyboard=True
)


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Style1'),
            KeyboardButton(text='Style2'),
            KeyboardButton(text='Style3'),
        ]
    ],
    resize_keyboard=True
)