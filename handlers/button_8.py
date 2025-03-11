import os
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import BadRequest

def count_files(folder_path):
    try:
        return len([
            name for name in os.listdir(folder_path)
            if os.path.isfile(os.path.join(folder_path, name))
        ])
    except FileNotFoundError:
        return 0

async def handle_button_8(query, context, users_data):
    # Count total users
    total_users = len(users_data)

    # Count media files
    art_files = count_files("content/art")
    video_files = count_files("content/video")
    gif_files = count_files("content/gif")

    message_text = (
        "<b>📊 General bot statistics:</b>\n\n"
        f"<b>🎨 Art:</b> <b>{art_files}</b>\n"
        f"<b>🎬 Video:</b> <b>{video_files}</b>\n"
        f"<b>🎥 GIF:</b> <b>{gif_files}</b>\n\n"
        f"<b>👥 All users:</b> <b>{total_users}</b>"
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
        print(f"Edit error: {e}")
        await query.message.reply_text("Failed to show statistics.")
