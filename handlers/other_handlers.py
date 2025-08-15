from keyboards.pagination_kb import create_pagination_keyboard
from handlers.main_handlers import init_dict
from handlers.main_handlers import users
from services.save_users_to_db import change_information_in_db, save_users

from aiogram.types import CallbackQuery, Message
from aiogram import Router, F


router = Router()


@router.callback_query(F.data == 'forward_right')
async def Forward_right_func(callback: CallbackQuery):
    users[str(callback.from_user.id)]['last_page'] += 1
    change_information_in_db(users)
    if int(list(init_dict.keys())[-1]) <= users[str(callback.from_user.id)]['last_page']:
        keyboard = create_pagination_keyboard(
            'forward_left', f'{users[str(callback.from_user.id)]['last_page']}/{list(init_dict.keys())[-1]}')
    else:
        keyboard = create_pagination_keyboard(
            'forward_left', f'{users[str(callback.from_user.id)]['last_page']}/{list(init_dict.keys())[-1]}', 'forward_right')
    await callback.message.answer(text=init_dict[str(users[str(callback.from_user.id)]['last_page'])], reply_markup=keyboard)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.delete()
    await callback.answer()


@router.callback_query(F.data == 'forward_left')
async def Forward_left_func(callback: CallbackQuery):
    users[str(callback.from_user.id)]['last_page'] -= 1
    change_information_in_db(users)
    if int(list(init_dict.keys())[0]) >= users[str(callback.from_user.id)]['last_page']:
        keyboard = create_pagination_keyboard(
            f'{users[str(callback.from_user.id)]['last_page']}/{list(init_dict.keys())[-1]}', 'forward_right')
    else:
        keyboard = create_pagination_keyboard(
            'forward_left', f'{users[str(callback.from_user.id)]['last_page']}/{list(init_dict.keys())[-1]}', 'forward_right')

    await callback.message.answer(text=init_dict[str(users[str(callback.from_user.id)]['last_page'])], reply_markup=keyboard)
    await callback.message.edit_reply_markup(reply_markup=None)
    await callback.message.delete()
    await callback.answer()


@router.callback_query(lambda x: '/' in x.data and x.data.replace('/', '').isdigit())
async def bookmarks_data(callback: CallbackQuery):
    users[str(callback.from_user.id)]['bookmarks'].append(
        f'страница {users[str(callback.from_user.id)]['last_page']}')
    change_information_in_db(users)
    await callback.answer(text='Закладка успешно добавлена!')


@router.callback_query(lambda x: 'страница' in x.data)
async def bookmark_callback(callback: CallbackQuery):
    page = callback.data.split()
    num_of_page = page[1]
    users[str(callback.from_user.id)]["last_page"] = int(num_of_page)
    save_users(users)
    if int(list(init_dict.keys())[0]) >= users[str(callback.from_user.id)]['last_page']:
        keyboard = create_pagination_keyboard(
            f'{users[str(callback.from_user.id)]['last_page']}/{list(init_dict.keys())[-1]}', 'forward_right')
    elif int(list(init_dict.keys())[-1]) <= users[str(callback.from_user.id)]['last_page']:
        keyboard = create_pagination_keyboard(
            'forward_left', f'{users[str(callback.from_user.id)]['last_page']}/{list(init_dict.keys())[-1]}')
    else:
        keyboard = create_pagination_keyboard(
            'forward_left', f'{users[str(callback.from_user.id)]['last_page']}/{list(init_dict.keys())[-1]}', 'forward_callback')
    await callback.message.answer(text=init_dict[num_of_page], reply_markup=keyboard)
    await callback.answer()
