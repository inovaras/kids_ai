import logging
from telegram import Bot, ReplyKeyboardMarkup
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, Filters, MessageHandler, CommandHandler
import requests
import os
from dotenv import load_dotenv

from consts import *

load_dotenv()
secret_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("CHAT_ID")

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


updater = Updater(token=secret_token)
bot = Bot(token=secret_token)

media_folder = "media"
file_list = os.listdir(media_folder)


def wake_up(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=manual,
    )
    buttons = ReplyKeyboardMarkup(
        [
            ["/last_selfy", "/high_school_photo", "/main_hobby", ],
            ["/tell_about_gpt_granny", "/tell_about_first_love", "/github_link"],
        ],
        resize_keyboard=True,
    )


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id, text=f"Привет, {chat.first_name}, я PrettyKittyBot"
    )


def send_photo(file_name):
    if file_name.endswith(".jpg") or file_name.endswith(".png"):
        file_path = os.path.join(media_folder, file_name)
        with open(file_path, "rb") as photo:
            bot.send_photo(chat_id=chat_id, photo=photo)


def send_audio(audio_name):
    url = f"https://api.telegram.org/bot{secret_token}/sendAudio"
    file_path = os.path.join(media_folder, audio_name)
    files = {"audio": open(file_path, "rb")}
    data = {"chat_id": chat_id}
    response = requests.post(url, files=files, data=data)
    print(response.json())


def give_last_selfy(update, context):
    send_photo("last_selfy.jpg")


def give_high_school_photo(update, context):
    send_photo("high_school_photo.jpg")


def give_main_hobby(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=text_about_hobbie,
    )


def tell_about_gpt_granny(update, context):
    send_audio("chat_gpt.wav")


def tell_about_first_love(update, context):
    send_audio("first_love.wav")


def send_github_link(update, context):

    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id, text=github_link
    )


def what_to_do_next(update, context):
    chat = update.effective_chat


def main():
    updater.dispatcher.add_handler(CommandHandler("start", wake_up))
    updater.dispatcher.add_handler(CommandHandler("last_selfy", give_last_selfy))
    updater.dispatcher.add_handler(
        CommandHandler("high_school_photo", give_high_school_photo)
    )
    updater.dispatcher.add_handler(CommandHandler("main_hobby", give_main_hobby))
    updater.dispatcher.add_handler(
        CommandHandler("tell_about_gpt_granny", tell_about_gpt_granny)
    )
    updater.dispatcher.add_handler(
        CommandHandler("tell_about_first_love", tell_about_first_love)
    )
    updater.dispatcher.add_handler(CommandHandler("github_link", send_github_link))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, say_hi))
    updater.dispatcher.add_handler(CommandHandler("nextstep", what_to_do_next))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
