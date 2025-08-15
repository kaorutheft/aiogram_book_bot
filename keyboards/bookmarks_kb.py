from lexicon.lexicon import lexicon_bot

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_bookmarks_keyboard(*buttons: str) -> InlineKeyboardMarkup:
    inline_builder = InlineKeyboardBuilder()

    btn = [InlineKeyboardButton(
        text=lexicon_bot[button] if button in lexicon_bot else button, callback_data=button) for button in buttons]

    inline_builder.row(*btn, width=1)
    inline_builder.row(
        InlineKeyboardButton(
            text=lexicon_bot["edit_bookmarks_button"], callback_data="edit_bookmarks"
        ),
        InlineKeyboardButton(
            text=lexicon_bot["cancel"], callback_data="cancel"),
        width=2,
    )
    return inline_builder.as_markup()


def create_bookmarks_keyboard_edit(*buttons: str) -> InlineKeyboardMarkup:
    inline_builder = InlineKeyboardBuilder()

    btn = [InlineKeyboardButton(
        text=f'🗑{lexicon_bot[button]}' if button in lexicon_bot else f'🗑{button}', callback_data=f'🗑{button}') for button in buttons]

    inline_builder.row(*btn, width=1)
    inline_builder.row(
        InlineKeyboardButton(
            text=lexicon_bot['cancel'], callback_data='cancel_edit_bookmarks'
        ), width=1
    )
    return inline_builder.as_markup()
