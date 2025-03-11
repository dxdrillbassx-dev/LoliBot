import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, Message, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, CallbackContext, MessageHandler, filters
from config import TOKEN
from handlers.faq_handler import handle_faq
from handlers.button_1 import handle_button_1
from users_manager import load_users, save_users
from datetime import datetime
from handlers.random_media import handle_random_art, handle_buttons
from handlers.button_8 import handle_button_8
from handlers.button_7 import handle_button_coder
from admin_notifications import notify_admins_on_new_user

# Кнопки основного меню (8 кнопок)
def get_main_buttons() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton("Profile", callback_data='button_1')],
        [InlineKeyboardButton("Offer content", callback_data='button_2'),
         InlineKeyboardButton("Admin", url="https://t.me/kevinmitni")],
        [InlineKeyboardButton("FAQ", callback_data='button_4'),
         InlineKeyboardButton("Our chats", callback_data='button_5')],
        [InlineKeyboardButton("How it works", callback_data='button_6'),
         InlineKeyboardButton("Coder", callback_data='button_7')],
        [InlineKeyboardButton("Bot Statistic", callback_data='button_8')]
    ]
    return InlineKeyboardMarkup(keyboard)


# Команда /start
async def start(update: Update, context: CallbackContext) -> None:
    users_data = load_users()  # Загружаем данные пользователей

    # Проверяем, если пользователя нет в данных - добавляем
    user_id = update.message.from_user.id
    if user_id not in users_data:
        # Записываем дату первого запуска бота только если пользователя нет
        users_data[user_id] = {
            'registration_date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        save_users(users_data)  # Сохраняем данные только если нового пользователя добавили

    # Отправляем стикер с кнопками
    sticker_file_id = 'CAACAgIAAxkBAAEBIhxnyZ5to1Q3ZKhfU7WBJDt0yFaSMQAC0x4AAqpBIUiHxavpLp-YXTYE'  # Замените на свой file_id стикера
    keyboard = [
        [KeyboardButton("Random Art"), KeyboardButton("Random Video")],  # Random Art и Random Video в одном ряду
        [KeyboardButton("Random GIF")]  # Random GIF на отдельной строке
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

    # Отправляем стикер и текст с обычными кнопками
    await update.message.reply_sticker(sticker_file_id, reply_markup=reply_markup)

    # Отправляем инлайн кнопки
    await update.message.reply_text(
        '<b>Good choice! Welcome to this wonderful world! Just logged into the bot and missed everything that was thrown? Write /syncmedia and enjoy.</b>',
        reply_markup=get_main_buttons(),
        parse_mode="HTML"  # Включаем поддержку HTML
    )
    await notify_admins_on_new_user(update, context)

# Обработка инлайн-кнопок
async def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    await query.answer()
    data = query.data

    # Загружаем данные пользователей
    users_data = load_users()

    if data == 'start_button':
        if isinstance(query.message, Message):
            user = query.from_user
            first_name = user.first_name if user.first_name else "Not set"

            # Формируем приветственное сообщение с жирным именем
            welcome_message = f"<b>{first_name}, welcome to this wonderful world! Just logged into the bot and missed everything that was thrown? Write /syncmedia and enjoy.</b>"

            # Используем edit_message_text для плавного изменения текста
            await query.edit_message_text(
                welcome_message,
                parse_mode="HTML",  # Устанавливаем форматирование HTML
                reply_markup=get_main_buttons()
            )

    elif data == 'button_1':
        await handle_button_1(query, context, users_data)

    elif data == 'button_4':
        await handle_faq(query, context)

    elif data == 'button_8':
        await handle_button_8(query, context, users_data)

    elif data == 'button_7':
        await handle_button_coder(query, context)

    elif data == 'button_5':  # Обработка кнопки "Our chats"
        text = "<b>Our chats:</b>"

        # Кнопки для перехода в чаты и кнопка назад
        keyboard = [
            [
                InlineKeyboardButton("dxdrmusic", url="https://t.me/dxdrmusic"),
                InlineKeyboardButton("elementras", url="https://t.me/elementras")
            ],
            [
                InlineKeyboardButton("🔙 Back", callback_data='start_button')  # Кнопка Back
            ]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Используем edit_message_text для плавного изменения текста
        await query.edit_message_text(
            text,
            parse_mode="HTML",  # Устанавливаем форматирование HTML
            reply_markup=reply_markup
        )

    elif data == 'button_6':  # Обработка кнопки "How it works"
        text = (
            "<b>Every day, you will receive content (art, videos, etc.) in the bot's private messages. Also, if you just logged into the bot and skipped all the content, you can use the /syncmedia command. This will allow you to get all the content that was posted before you.</b>"
        )

        # Кнопки для Спамблока и других
        keyboard = [
            [InlineKeyboardButton("🔙 Back", callback_data='start_button')]  # Кнопка Back
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        # Используем edit_message_text для плавного изменения текста
        await query.edit_message_text(
            text,
            parse_mode="HTML",  # Устанавливаем форматирование HTML
            reply_markup=reply_markup
        )

    elif data == 'button_2':  # Обработка кнопки "Offer content"
        # Изменяем текст для кнопки "Offer content"
        text = (
            f"<b>Do you want to offer your content for publication? Feel free to write to me, I appreciate it! Spamblock? Click on the Spamblock button and I'll write to you myself.</b>"
        )
        # Кнопки для Спамблока и других (Spamblock и Admin в одном ряду)
        keyboard = [
            [
                InlineKeyboardButton("Spamblock", callback_data='spamblock'),
                InlineKeyboardButton("Admin", url="https://t.me/kevinmitni")
            ],
            [InlineKeyboardButton("🔙 Back", callback_data='start_button')]  # Кнопка Back на новой строке
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        # Используем edit_message_text для плавного изменения текста
        await query.edit_message_text(
            text,
            reply_markup=reply_markup,
            parse_mode="HTML"  # Включаем поддержку HTML
        )

    elif data == 'button_5':
        await handle_button_1(query, context, users_data)

    elif data.startswith('button_'):
        number = data.split('_')[1]

        # Удаляем предыдущее сообщение
        if isinstance(query.message, Message):
            try:
                await query.message.delete()
            except Exception as e:
                print(f"Ошибка удаления: {e}")

        # Создаём клавиатуру без доп.
        keyboard = [[InlineKeyboardButton("🔙 Back", callback_data='start_button')]]

        reply_markup = InlineKeyboardMarkup(keyboard)

        # Отправка нового сообщения с использованием edit_message_text
        await query.edit_message_text(
            text=f"You selected Button {number}",
            reply_markup=reply_markup
        )

    # Обработка доп.
    elif data.startswith('extra1_') or data.startswith('extra2_'):
        extra_info = data.split('_')
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text=f"You pressed {extra_info[0].upper()} from button {extra_info[1]}"
        )

    # Обработка кнопки Spamblock
    elif data == 'spamblock':
        await context.bot.send_message(
            chat_id=query.from_user.id,
            text="I'll write to you myself soon! Stay tuned!"
        )

    elif data == 'random_art':  # Обработка кнопки Random Art
        await handle_random_art(update, context)

def main() -> None:
    application = Application.builder().token(TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button))
    application.add_handler(MessageHandler(filters.TEXT, handle_buttons))

    application.run_polling()


if __name__ == '__main__':
    main()