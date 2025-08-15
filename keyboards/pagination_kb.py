from lexicon.lexicon import lexicon_bot

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_pagination_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    inline_builder = InlineKeyboardBuilder()

    btn = [InlineKeyboardButton(
        text=lexicon_bot[button] if button in lexicon_bot else button, callback_data=button) for button in buttons]

    inline_builder.row(*btn)

    return inline_builder.as_markup()
