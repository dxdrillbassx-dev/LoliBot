from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.error import BadRequest

async def handle_button_1(query, context, users_data):
    user = query.from_user
    user_id = user.id

    # Get registration date if exists
    registration_date = users_data.get(str(user_id), {}).get('registration_date', "Not available")

    # Format profile message
    profile_info = (
        "<b>🪪 Your Profile</b>\n\n"
        f"<b>📝 Name:</b> <b>{user.first_name if user.first_name else 'Not set'}</b>\n"
        f"<b>🆔 ID:</b> <b>{user.id}</b>\n"
        f"<b>📆 Registration Date:</b> <b>{registration_date}</b>"
    )

    # Create "Back" button
    keyboard = [
        [InlineKeyboardButton("🔙 Back", callback_data='start_button')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    # Try to edit the message
    try:
        await query.edit_message_text(
            text=profile_info,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    except BadRequest as e:
        print(f"Edit error: {e}")
        await query.message.reply_text("Failed to update profile information.")
