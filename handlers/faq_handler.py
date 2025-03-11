from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.error import BadRequest

async def handle_faq(query, context):
    faq_text = """
1. All images, videos, and other works of art published by the bot feature exclusively characters who are of legal age (18+);

2. Use of the bot is permitted only for individuals who have reached the age of majority according to the laws of their country;

3. The bot’s author is not associated with the content published by the bot and bears no responsibility for its origin or content;

4. Users are fully responsible for how they use materials obtained through the bot, including any violation of the laws of their country of residence;

5. Any attempt to upload, distribute, or publish illegal, offensive, or prohibited content through the bot is strictly forbidden;

6. All materials distributed through the bot remain the property of their respective creators. In the event of copyright infringement, rights holders may request the removal of the materials;

7. The bot’s author reserves the right to temporarily or permanently restrict user access to the bot for violating this agreement;

8. This user agreement may be modified at any time. By continuing to use the bot after changes are made, you agree to the new version of the agreement;

9. In the event of disputes related to the use of the bot, the laws of the United States of America shall apply;
    """

    faq_text = f"```{faq_text}```"

    keyboard = [
        [InlineKeyboardButton("🔙 Back", callback_data='start_button')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Попробуем редактировать сообщение
    try:
        await query.edit_message_text(
            text=faq_text,
            reply_markup=reply_markup,
            parse_mode='Markdown'
        )
    except BadRequest as e:
        # Если сообщение не найдено, выводим ошибку
        print(f"Ошибка редактирования: {e}")
        # Можно добавить обработку, например, отправить новое сообщение, если редактирование не удается
        await query.message.reply_text("Не удалось обновить информацию.")
