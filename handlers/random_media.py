import os
import random
from telegram import Update
from telegram.ext import CallbackContext

async def handle_random_art(update: Update, context: CallbackContext) -> None:
    art_folder = 'content/art'
    files = os.listdir(art_folder)
    images = [file for file in files if file.endswith(('.jpg', '.jpeg', '.png'))]

    if images:
        random_image = random.choice(images)
        file_path = os.path.join(art_folder, random_image)
        with open(file_path, 'rb') as photo:
            await update.message.reply_photo(photo=photo)
    else:
        await update.message.reply_text("No art available.")

async def handle_random_video(update: Update, context: CallbackContext) -> None:
    video_folder = 'content/video'
    files = os.listdir(video_folder)
    videos = [file for file in files if file.endswith(('.mp4', '.avi', '.mov'))]

    if videos:
        random_video = random.choice(videos)
        file_path = os.path.join(video_folder, random_video)
        with open(file_path, 'rb') as video:
            await update.message.reply_video(video=video)
    else:
        await update.message.reply_text("No video available.")

async def handle_random_gif(update: Update, context: CallbackContext) -> None:
    gif_folder = 'content/gif'
    files = os.listdir(gif_folder)
    gifs = [file for file in files if file.endswith('.gif')]

    if gifs:
        random_gif = random.choice(gifs)
        file_path = os.path.join(gif_folder, random_gif)
        with open(file_path, 'rb') as gif:
            await update.message.reply_animation(animation=gif)
    else:
        await update.message.reply_text("No GIF available.")

async def handle_buttons(update: Update, context: CallbackContext) -> None:
    text = update.message.text
    if text == "Random Art":
        await handle_random_art(update, context)
    elif text == "Random Video":
        await handle_random_video(update, context)
    elif text == "Random GIF":
        await handle_random_gif(update, context)