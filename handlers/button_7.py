from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import BadRequest

async def handle_button_coder(query, context):
    message_text = (
        "<b>Yes, I'm the coolest and fucking coder of this beautiful bot, "
        "if you don't like something about the bot, please keep quiet about it, "
        "my bot is perfect (joke).</b>\n\n"
        "<b>My own account:</b> <b><a href='https://t.me/kevinmitni'>kevinmitni</a></b>\n\n"
        "<b>I also have my personal channel, where I often post my other projects "
        "(prefer loli content heh)</b>\n"
        "<b>Creator's channel:</b> <b><a href='https://t.me/dxdrmusic'>@dxdrmusic</a></b>"
    )

    keyboard = [
        [InlineKeyboardButton("🔙 Back", callback_data='start_button')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    try:
        await query.edit_message_text(
            text=message_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    except BadRequest as e:
        print(f"Ошибка редактирования: {e}")
        await query.message.reply_text("Не удалось показать информацию о кодере.")
