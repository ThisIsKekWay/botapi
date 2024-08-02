from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

get = KeyboardButton(text="Получить сообщения")
post = KeyboardButton(text="Написать сообщение")
main_kb = ReplyKeyboardMarkup(keyboard=[[get], [post]], one_time_keyboard=True, resize_keyboard=True)


def create_pagination_keyboard(current_page: int, size: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    if current_page > 1:
        builder.button(text="⬅️ Назад", callback_data=f"page_{current_page - 1}")

    builder.button(text=f"{current_page}", callback_data="current_page")

    if size == 10:
        builder.button(text="Вперед ➡️", callback_data=f"page_{current_page + 1}")

    return builder.as_markup()
