from aiogram.types import (
    ReplyKeyboardRemove,
    ReplyKeyboardMarkup,
    KeyboardButton,
)

phone = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Поделиться номером телефона", request_contact=True)
        ]
    ],
    resize_keyboard=True
)

rmk = ReplyKeyboardRemove()