import logging
import os

import requests
from dotenv import load_dotenv
from telegram import Bot, ReplyKeyboardMarkup, ext
from telegram.ext import CommandHandler, Filters, MessageHandler, Updater


from consts import *

load_dotenv()
secret_token = os.getenv("TELEGRAM_TOKEN")
chat_id = os.getenv("CHAT_ID")
ibm_api_key = os.getenv('IBM_API_KEY')


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)


updater = Updater(token=secret_token)
bot = Bot(token=secret_token)

media_folder = "media"
file_list = os.listdir(media_folder)


def recognize_speech(audio_file_path):
    url = "https://api.us-south.speech-to-text.watson.cloud.ibm.com/instances/YOUR_INSTANCE_ID/v1/recognize"
    headers = {
        "Content-Type": "audio/ogg",
    }
    params = {
        "access_token": ibm_api_key,
        "model": "en-US_BroadbandModel",  # Используйте код модели для вашего языка, если это не английский
    }

    with open(audio_file_path, "rb") as audio_file:
        audio_data = audio_file.read()

    response = requests.post(url, headers=headers, params=params, data=audio_data)

    if response.status_code == 200:
        return response.json()["results"][0]["alternatives"][0]["transcript"]
    else:
        return None


def handle_voice_message(update, context):
    # Получить объект аудио-сообщения из обновления
    voice_message = update.message.voice

    # Загрузить аудио на сервер Telegram и получить объект File
    voice_file = voice_message.get_file()

    # Скачать аудио-файл на локальную машину
    audio_file_path = 'audio.ogg'
    voice_file.download(audio_file_path)

    # Распознать речь с использованием IBM Watson Speech to Text API
    recognized_text = recognize_speech(audio_file_path)

    if recognized_text:
        # Отправить распознанный текст пользователю
        update.message.reply_text("Распознанная речь: " + recognized_text)
    else:
        update.message.reply_text("Не удалось распознать речь.")


def wake_up(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id,
        text=manual,
    )
    buttons = ReplyKeyboardMarkup(
        [
            [
                "/last_selfie",
                "/high_school_photo",
                "/main_hobby",
            ],
            ["/tell_about_gpt_granny", "/SQLvsNoSQL", "/tell_about_first_love"],
            ["/nextstep", "/history", "/github_link"],
            ["/newcat", "/newdog"]
        ],
        resize_keyboard=True,
    )


def say_hi(update, context):
    chat = update.effective_chat
    context.bot.send_message(
        chat_id=chat.id, text=f"Привет, {chat.first_name}"
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


def give_last_selfie(update, context):
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
    context.bot.send_message(chat_id=chat.id, text=github_link)


def next_step(update, context):
    next_steps_message = "Пожалуйста, напишите Ваше сообщение"
    context.bot.send_message(chat_id=chat_id, text=next_steps_message)



def echo(update, context):
    if update.message.from_user.is_bot:
        return
    # Отправьте ответное сообщение, чтобы бот не пропустил сообщение от себя
    chat = update.effective_chat
    with open("messages/text.txt", mode="a", encoding="utf-8") as file:
        file.write(update.message.text + '\n')
    context.bot.send_message(chat_id=chat_id, text="Спасибо за сообщение!")


def get_history(update, context):
    with open("messages/text.txt", mode="r", encoding="utf-8") as file:
        text = file.read()
    context.bot.send_message(chat_id=chat_id, text=text)


message_handler = MessageHandler(Filters.text, echo)


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
    return response[0]['url']

def main():
    updater.dispatcher.add_handler(CommandHandler("start", wake_up))
    updater.dispatcher.add_handler(CommandHandler("last_selfie", give_last_selfie))
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
    updater.dispatcher.add_handler(CommandHandler('nextstep', next_step))
    updater.dispatcher.add_handler(CommandHandler('history', get_history))
    updater.dispatcher.add_handler(CommandHandler('newcat', give_new_cat))
    updater.dispatcher.add_handler(CommandHandler('newdog', give_new_dog))
    updater.dispatcher.add_handler(message_handler)

    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()
