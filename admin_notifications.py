from telegram import Bot
from config import ADMIN_IDS
from users_manager import load_users

# Функция для оповещения администраторов о новом пользователе
async def notify_admins_on_new_user(update, context):
    user_id = update.message.from_user.id
    first_name = update.message.from_user.first_name or "Unknown User"
    username = update.message.from_user.username  # Получаем username пользователя (если есть)
    bot = Bot(token=context.bot.token)

    # Получаем количество пользователей с помощью функции load_users
    users_data = load_users()
    total_users = len(users_data)

    # Формируем кликабельное имя пользователя (если есть username)
    if username:
        user_link = f"[{first_name}](tg://user?id={user_id})"
    else:
        user_link = f"{first_name}"  # Если нет username, просто имя

    # Перебираем список администраторов и отправляем уведомление каждому
    for admin_id in ADMIN_IDS:
        try:
            message = (
                f"🪞 A new user has entered your bot!\n"
                f"🆔 {user_id} {user_link}\n\n"
                f"💠 Total users in the bot: {total_users}"
            )
            await bot.send_message(admin_id, message, parse_mode="Markdown")
        except Exception as e:
            print(f"Error sending message to admin {admin_id}: {e}")
