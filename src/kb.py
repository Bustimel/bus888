from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def yes_no_kb():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Так", callback_data="confirm_yes"),
            InlineKeyboardButton(text="🔁 Ні / Навпаки", callback_data="confirm_no")
        ]
    ])