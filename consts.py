import os

from dotenv import load_dotenv

load_dotenv()
my_hobby = os.getenv("my_hobby")

URL_CAT = "https://api.thecatapi.com/v1/images/search"
URL_DOG = "https://api.thedogapi.com/v1/images/search"
github_link = "https://github.com/inovaras/kids_ai"
text_about_hobby = my_hobby
manual = f"""
Ознакомьтесь с руководством.
Вы можете посылать следующие команды:

Получить фото:
/last_selfie - последнее селфи
/school_photo - школьная фотография

Прочитать обо мне:
/main_hobby - небольшой пост о моём главном увлечении

Прослушать войс:
/gpt_granny - рассказ в формате «объясняю своей бабушке», что такое GPT 
/SQLvsNoSQL - максимально короткое объяснение разницы между SQL и NoSQL
/first_love - история первой любви 

Получить ссылки:
/github_link - ссылка на репозиторий в гитхабе 

Ещё две полезные команды:
/nextstep - ввести текст о дальнейших шагах
/check_message - проверить, есть ли сообщение о дальнейших шагах

И просто повеселиться:
/newcat - получить фотку нового котика
/newdog - получить фотку новой собачки

А также:
Внизу, для удобства, есть терминал с кнопками и меню с командами, попробуйте :)
"""
