import logging
import os

import requests
from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup, ext
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater

from consts import *

load_dotenv()
secret_token = os.getenv("TELEGRAM_TOKEN")


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


updater = Updater(token=secret_token)
bot = Bot(token=secret_token)

media_folder = "media"
file_list = os.listdir(media_folder)
is_used_command_next_step = False


def wake_up(update, context):
    chat = update.effective_chat
    buttons = ReplyKeyboardMarkup(
        [
            [
                "/last_selfie",
                "/school_photo",
                "/main_hobie",
            ],
            ["/gpt_granny", "/SQLvsNoSQL", "/first_love"],
            ["/voice_to_text"],
            ["/nextstep", "/check_message", "/github_link"],
            ["/newcat", "/newdog"],
        ],
        resize_keyboard=True,
    )
    chat.bot.send_message(chat_id=chat.id, text=manual, reply_markup=buttons)


def send_photo(update, file_name):
    chat = update.effective_chat
    if file_name.endswith(".jpg") or file_name.endswith(".png"):
        file_path = os.path.join(media_folder, file_name)
        with open(file_path, "rb") as photo:
            chat.send_photo(photo=photo)


def send_voice(update, audio_name):
    chat = update.effective_chat
    file_path = os.path.join(media_folder, audio_name)
    with open(file_path, "rb") as audio_file:
        bot.send_voice(chat_id=chat.id, voice=audio_file)


def give_last_selfie(update, context):
    send_photo(update, "last_selfie.jpg")


def give_high_school_photo(update, context):
    send_photo(update, "school_photo.jpg")


def give_main_hobie(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=text_about_hobie,
    )


def tell_about_gpt_granny(update, context):
    send_voice(update, "chat_gpt.mp3")


def tell_about_sql_vs_nosql(update, context):
    send_voice(update, "sql_vs_nosql.mp3")


def tell_about_first_love(update, context):
    send_voice(update, "first_love.mp3")


def send_github_link(update, context):
    chat = update.effective_chat
    context.bot.send_message(chat_id=chat.id, text=github_link)


def next_step(update, context):
    chat = update.effective_chat
    next_steps_message = "Пожалуйста, напишите дальнейшие шаги"
    bot.send_message(chat_id=chat.id, text=next_steps_message)
    global is_used_command_next_step
    is_used_command_next_step = True


def echo(update, context):
    chat = update.effective_chat
    global is_used_command_next_step
    if update.message.from_user.is_bot or not is_used_command_next_step:
        return

    with open("messages/text.txt", mode="a", encoding="utf-8") as file:
        file.write(update.message.text + "\n")
    bot.send_message(chat_id=chat.id, text="Спасибо за сообщение!")
    is_used_command_next_step = False


def check_message(update, context):
    chat = update.effective_chat
    with open("messages/text.txt", mode="r", encoding="utf-8") as file:
        text = file.read()
    bot.send_message(chat_id=chat.id, text=text)


def voice_to_text(update, context):
    pass


def give_new_cat(update, context):
    chat = update.effective_chat
    chat.send_photo(get_new_image(URL_CAT, URL_DOG))


def give_new_dog(update, context):
    chat = update.effective_chat
    chat.send_photo(get_new_image(URL_DOG, URL_CAT))


def get_new_image(URL_1, URL_2):
    try:
        response = requests.get(URL_1).json()
    except Exception as e:
        print(e)
        response = requests.get(URL_2).json()
    return response[0]["url"]


def main():
    updater.dispatcher.add_handler(CommandHandler("start", wake_up))
    updater.dispatcher.add_handler(CommandHandler("last_selfie", give_last_selfie))
    updater.dispatcher.add_handler(
        CommandHandler("school_photo", give_high_school_photo)
    )
    updater.dispatcher.add_handler(CommandHandler("main_hobie", give_main_hobie))
    updater.dispatcher.add_handler(CommandHandler("gpt_granny", tell_about_gpt_granny))
    updater.dispatcher.add_handler(
        CommandHandler("SQLvsNoSQL", tell_about_sql_vs_nosql)
    )
    updater.dispatcher.add_handler(CommandHandler("first_love", tell_about_first_love))
    updater.dispatcher.add_handler(CommandHandler("github_link", send_github_link))
    updater.dispatcher.add_handler(CommandHandler("nextstep", next_step))
    updater.dispatcher.add_handler(CommandHandler("check_message", check_message))
    updater.dispatcher.add_handler(CommandHandler("voice_to_text", voice_to_text))
    updater.dispatcher.add_handler(CommandHandler("newcat", give_new_cat))
    updater.dispatcher.add_handler(CommandHandler("newdog", give_new_dog))
    updater.dispatcher.add_handler(MessageHandler(Filters.text, echo))
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
