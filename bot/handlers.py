import json

from typing import Union

from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.utils.formatting import Bold, Text

from DAO import MessageDAO, db
from aiogram import types, Router, F

from FSM import MessageStates
from keyboards import main_kb, create_pagination_keyboard
from misc import redis

rt = Router()
dao = MessageDAO(db)


@rt.message(CommandStart())
async def start(msg: types.Message, state: FSMContext):
    content = Text(f"Привет ", Bold(msg.from_user.full_name), "!\nВыбери, что будем делать?")
    await msg.answer(**content.as_kwargs(), reply_markup=main_kb)
    await state.set_state(MessageStates.main_menu)


@rt.message(F.text == 'Написать сообщение')
async def post_messages(msg: types.Message, state: FSMContext):
    await msg.answer("Введите и отправьте сообщение")
    await state.set_state(MessageStates.post_msgs)


@rt.message(F.text, StateFilter(MessageStates.post_msgs))
async def write_message(msg: types.Message, state: FSMContext):
    data = {"author_tg_id": msg.from_user.id, "text": msg.text}
    await dao.insert(data)
    cache = await redis.keys("*")
    if cache:
        last_key = max(cache).decode("utf-8")
        last_cache = await redis.get(last_key)
        if len(last_cache.decode("utf-8").split("\n")) < 10:
            await redis.delete(last_key)
    await msg.answer(f'Сообщение сохранено', reply_markup=main_kb)
    await state.set_state(MessageStates.main_menu)


@rt.callback_query(F.data.startswith('page_'))
@rt.message(F.text == 'Получить сообщения')
async def process_messages_or_pagination(event: Union[types.Message, types.CallbackQuery], page: int = 1):
    page_size = 10
    if isinstance(event, types.CallbackQuery):
        callback_query = event
        page = int(callback_query.data.split('_')[1])

    cached_messages = await redis.get(f'cached_messages_page_{page}')
    if cached_messages:
        cached_messages = json.loads(cached_messages.decode('utf-8'))
    else:
        cached_messages = []
        msgs = await dao.get_msg_with_pagination(page, page_size)
        page = msgs[0].get("page")
        for message in msgs[1:]:
            message.pop("_id", None)
            formatted_msg = {'Author ID': message['author_tg_id'], 'Text': message['text']}
            cached_messages.append(formatted_msg)
        formatted_msgs_str = json.dumps(cached_messages)
        await redis.set(f'cached_messages_page_{page}', formatted_msgs_str)

    formatted_msgs = [f"АвторID: {item['Author ID']}, Text: {item['Text']}" for item in cached_messages]
    formatted_output = '\n'.join(formatted_msgs)
    keyboard = create_pagination_keyboard(page, len(formatted_msgs))

    if isinstance(event, types.Message):
        await event.answer(formatted_output, reply_markup=keyboard)
    elif isinstance(event, types.CallbackQuery):
        if formatted_output:
            await event.message.edit_text(formatted_output, reply_markup=keyboard)
        else:
            await event.answer("Дальше пусто")
