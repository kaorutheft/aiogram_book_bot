import json
from keyboards.bookmarks_kb import create_bookmarks_keyboard
from keyboards.pagination_kb import create_pagination_keyboard
from services.save_users_to_db import save_users
from lexicon.lexicon import lexicon_bot

from aiogram.enums import ParseMode
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, CommandStart

router = Router()

try:
    with open('database\\database.json', 'r', encoding='utf-8') as file:
        users = json.load(file)
except (FileNotFoundError, json.decoder.JSONDecodeError):
    users = {}

try:
    with open('services\\init_book.json', 'r', encoding='utf-8') as file_init_book:
        init_dict = json.load(file_init_book)
except (FileNotFoundError, json.decoder.JSONDecodeError, UnicodeDecodeError):
    init_dict = {}


@router.message(CommandStart())
async def start_cmd(message: Message):
    global users
    user_id = str(message.from_user.id)
    if user_id not in users.keys():
        users[user_id] = {
            'last_page': 1,
            'bookmarks': []
        }
        save_users(users)
    await message.answer(text=lexicon_bot['start'], parse_mode=ParseMode.HTML)


@router.message(Command('help'))
async def start_cmd(message: Message):
    await message.answer(text=lexicon_bot['help'], parse_mode=ParseMode.HTML)


@router.message(Command('beginning'))
async def beggining_cmd(message: Message):
    users[str(message.from_user.id)]['last_page'] = 1
    save_users(users)
    keyboard = create_pagination_keyboard(
        f'{users[str(message.from_user.id)]['last_page']}/{list(init_dict.keys())[-1]}', 'forward_right')
    await message.answer(text=init_dict['1'], reply_markup=keyboard)


@router.message(Command('continue'))
async def continue_cmd(message: Message):
    if int(list(init_dict.keys())[0]) >= users[str(message.from_user.id)]['last_page']:
        keyboard = create_pagination_keyboard(
            f'{users[str(message.from_user.id)]['last_page']}/{list(init_dict.keys())[-1]}', 'forward_right')
    elif int(list(init_dict.keys())[-1]) <= users[str(message.from_user.id)]['last_page']:
        keyboard = create_pagination_keyboard(
            'forward_left', f'{users[str(message.from_user.id)]['last_page']}/{list(init_dict.keys())[-1]}')
    else:
        keyboard = create_pagination_keyboard(
            'forward_left', f'{users[str(message.from_user.id)]['last_page']}/{list(init_dict.keys())[-1]}', 'forward_right')
    await message.answer(text=init_dict[str(users[str(message.from_user.id)]['last_page'])], reply_markup=keyboard)


@router.message(Command('bookmarks'))
async def continue_cmd(message: Message):
    if len(users[str(message.from_user.id)]['bookmarks']) == 0:
        await message.answer('Список закладок пустой!')
        await message.answer()
        await message.message.delete()
    else:
        inline_kb = create_bookmarks_keyboard(
            *users[str(message.from_user.id)]['bookmarks'])
        await message.answer(text='Список доступных закладок:', reply_markup=inline_kb)
