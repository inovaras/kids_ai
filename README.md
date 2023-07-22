# kids_ai
Python бот для Телеграмм, который позволяет представить себя

### Как запустить проект:

Клонировать репозиторий:

```
git clone git@github.com:inovaras/kids_ai.git
```

Перейти в него в командной строке:
```
cd kids_ai
```

Cоздать и активировать виртуальное окружение:

```
python -m venv env
```

```
source venv/Scripts/activate
```

```
python -m pip install --upgrade pip
```

Установить зависимости из файла requirements.txt:

```
pip install -r requirements.txt
```
В корневой папке создайте файл  ```.env```
В файле ```.env``` создайте переменные TELEGRAM_TOKEN, CHAT_ID, my_hobie

В корневой папке создайте директорию media, положите туда файлы chat_gpt.mp3, first_love.mp3, last_selfie.jpg, school_photo.jpg

Запустите bot.py