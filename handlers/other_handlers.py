from keyboards.pagination_kb import create_pagination_keyboard
from keyboards.bookmarks_kb import create_bookmarks_keyboard_edit, create_bookmarks_keyboard
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


@router.callback_query(lambda x: '🗑' in x.data)
async def bookmark_callback(callback: CallbackQuery):
    del_page = callback.data.split()
    o = [i.split() for i in users[str(callback.from_user.id)]['bookmarks']]
    for i in range(len(o)):
        if o[i][1] == del_page[1]:
            users[str(callback.from_user.id)]['bookmarks'].remove(
                f'страница {del_page[1]}')
            save_users(users)
    await callback.answer('Успех')


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
            'forward_left', f'{users[str(callback.from_user.id)]['last_page']}/{list(init_dict.keys())[-1]}', 'forward_right')
    await callback.message.answer(text=init_dict[num_of_page], reply_markup=keyboard)
    await callback.answer()


@router.callback_query(F.data == 'cancel')
async def bookmark_callback(callback: CallbackQuery):
    await callback.message.delete()
    await callback.message.answer('/continue - продолжить чтение\n/help - другие доступные команды')


@router.callback_query(F.data == "edit_bookmarks")
async def bookmark_callback(callback: CallbackQuery):
    await callback.message.delete()
    keyboard = create_bookmarks_keyboard_edit(
        *users[str(callback.from_user.id)]['bookmarks'])
    await callback.message.answer(text='Выберите закладку, которую желаете удалить.', reply_markup=keyboard)


@router.callback_query(F.data == 'cancel_edit_bookmarks')
async def bookmark_callback(callback: CallbackQuery):
    if len(users[str(callback.from_user.id)]['bookmarks']) == 0:
        await callback.message.answer('Список закладок пуст!')
        await callback.answer()
        await callback.message.delete()
    else:
        inline_kb = create_bookmarks_keyboard(
            *users[str(callback.from_user.id)]['bookmarks'])
        await callback.message.answer(text='Список доступных закладок:', reply_markup=inline_kb)
        await callback.answer()
        await callback.message.delete()
