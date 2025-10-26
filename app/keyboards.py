from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_info_keyboard() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с кнопками для различных информационных разделов.
    
    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками "Контакты",
                              "Адреса отделений" и "Частые вопросы".
    """
    # Инициализируем билдер клавиатуры
    builder = InlineKeyboardBuilder()

    # Создаем кнопки с текстом и уникальными колбэк-данными
    button_contacts = InlineKeyboardButton(
        text="Контакты",
        callback_data="info_contacts"
    )
    button_addresses = InlineKeyboardButton(
        text="Адреса отделений",
        callback_data="info_addresses"
    )
    button_faq = InlineKeyboardButton(
        text="Частые вопросы",
        callback_data="info_faq"
    )
    
    # Добавляем кнопки в билдер
    builder.row(button_contacts, button_addresses, button_faq)

    # Возвращаем готовую клавиатуру
    return builder.as_markup()
