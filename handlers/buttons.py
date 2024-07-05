from aiogram.types import KeyboardButton, ReplyKeyboardMarkup


class ReplyKeyboard:
    text_or_voice_answer = ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💬🤖🎙️ Voice answers"),
                KeyboardButton(text="💬🤖💬 Text answers")
            ]
        ],
        resize_keyboard=True,
    )
    choosing_chat = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="😟 chat about anxiety 🤖")],
            [KeyboardButton(text="📷 chat to determine mood from photo 🤖")],
            [KeyboardButton(text="Back")]
        ],
        resize_keyboard=True,
    )
    back = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Back")]],
        resize_keyboard=True,
    )
