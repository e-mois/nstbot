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
            KeyboardButton(text='wave'),
            KeyboardButton(text='starry_night'),
            KeyboardButton(text='mosaic'),
        ],
        [
            KeyboardButton(text='pencil'),
            KeyboardButton(text='mosaic_ducks'),
            KeyboardButton(text='candy'),
        ],
        [
            KeyboardButton(text='udnie'),
            KeyboardButton(text='the_scream'),
            KeyboardButton(text='strip'),
        ],
        [
            KeyboardButton(text='seated-nude'),
            KeyboardButton(text='frida_kahlo'),
            KeyboardButton(text='feathers'),
        ]
    ],
    resize_keyboard=True
)
