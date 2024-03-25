import logging
import telebot
# Импортируем фаил GPT для отправки заапроса
from Gpt_3 import GPT
# Библиотека для кнопочек
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, Message
from config_3 import TOKEN
import json
import sqlite3

# Если в текущей директории нет файла db.sqlite -
# он будет создан; одновременно будет создано и соединение с базой данных
# Если файл существует, метод connect просто подключится к базе
con = sqlite3.connect('sqlite_story.db', check_same_thread=False)

# Создаём специальный объект cursor для работы с БД
# Вся дальнейшая работа будет вестись через методы этого объекта: cur
cur = con.cursor()

# ЗДЕСЬ БУДЕТ ПРОИСХОДИТЬ САМА РАБОТА С БАЗОЙ: ОТПРАВКА ЗАПРОСОВ, ПОЛУЧЕНИЕ ОТВЕТОВ
# Готовим SQL-запрос
# Для читаемости запрос обрамлён в тройные кавычки и разбит построчно
query = '''
CREATE TABLE IF NOT EXISTS user_story(
    user_id INTEGER PRIMARY KEY,
    genre TEXT,
    character TEXT,
    setting TEXT,
    user_request TEXT,
    story TEXT
);
'''
cur.execute(query)
con.commit()

# подключаемся к
gpt = GPT(system_content="Генерирует рассказ")

# Путь к файлу с логами ошибок
ERROR_LOG_FILE = 'error.log'

# токен
bot = telebot.TeleBot(TOKEN)

CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]

command_type = ""

# Кнопочка
markup = ReplyKeyboardMarkup(resize_keyboard=True)
markup.add(KeyboardButton('/help'))


# Обработчик команды /debug
@bot.message_handler(commands=['debug'])
def handle_debug(message):
    # Отправляем файл с логами ошибок
    with open(ERROR_LOG_FILE, 'rb') as file:
        bot.send_document(message.chat.id, file)


# пишем обработку /start
@bot.message_handler(commands=['start'])
def repeat_message(message):
    bot.send_message(message.chat.id, text=f"Привет, {message.from_user.first_name}, я бот сочинитель\n"
                                           "Помогу помочь написать рассказ\n"
                                           "Чтобы ознакомиться с командами напиши /help\n", reply_markup=markup)
    user_id_session = message.from_user.id
    print(user_id_session)
    cur = con.cursor()

    query = f'SELECT user_id FROM user_story WHERE user_id = {user_id_session}'
    print(query)
    results = cur.execute(query).fetchone()
    if results is None:
        query = f"INSERT INTO user_story VALUES ({user_id_session}, '', '','','','', '')"
        con.execute(query)
        print(query)
        con.commit()
    else:
        print('Эта сессия уже есть')
        query = f"select * from user_story WHERE user_id = {user_id_session}"
        results = cur.execute(query).fetchone()
        print(results)
        i = 0
        set_of_items = ("user_id_session", "user_genre", "user_pol", "user_character", "user_setting", "user_request", "story")
        for result in results:
            if set_of_items[i] == "user_genre":
                user_genre = results[i]
            if set_of_items[i] == "user_pol":
                user_pol = results[i]
            elif set_of_items[i] == "user_character":
                user_character = results[i]
            elif set_of_items[i] == "user_setting":
                user_setting = results[i]
            elif set_of_items[i] == "user_request":
                user_request = results[i]
            elif set_of_items[i] == "story":
                story = results[i]
            i += 1


# пишем обработку /help
@bot.message_handler(commands=['help'])
def help_message(message):
    # кнопочки для выбора предмета
    button_1 = telebot.types.KeyboardButton("/genre")
    bot.send_message(message.chat.id, text="Для того что бы начать\n"
                                           "Жми на кнопочки и выбирай\n"
                                           "/genre - начать\n",
                     reply_markup=telebot.types.ReplyKeyboardMarkup().add(button_1))


@bot.message_handler(commands=['genre'])
def genre (message):
    global command_type
    command_type = "genre"
    button_2 = telebot.types.KeyboardButton("Сказка")
    button_3 = telebot.types.KeyboardButton("Комедия")
    button_4 = telebot.types.KeyboardButton("Фантастика")
    button_5 = telebot.types.KeyboardButton("Ужастики")

    bot.send_message(message.chat.id, text="Вбери жанр рассказа:\n"
                                           "1)Сказка\n"
                                           "2)Комедия\n"
                                           "3)Фантастика\n"
                                           "4)Ужастики\n",
                     reply_markup=telebot.types.ReplyKeyboardMarkup().add(button_2, button_3, button_4, button_5,))

@bot.message_handler(commands=['character'])
def character (message):
    global command_type
    command_type = "character"
    button_18 = telebot.types.KeyboardButton("Доктор Стренч")
    button_19 = telebot.types.KeyboardButton("Гермиона Грейнджер")
    button_20 = telebot.types.KeyboardButton("Юлий (Три Богатыря)")
    button_21 = telebot.types.KeyboardButton("Золушка")
    bot.send_message(message.chat.id, text="Выбери  персонажа:\n"
                                           "1) Доктор Стренч\n"
                                           "2) Гермиона Грейнджер\n"
                                           "3) Юлий (Три Богатыря)\n"
                                           "4) Золушка\n"
                                            "Только тихо, что бы никто не заметил, ты можешь написать персонажа которого нету в списке 🤫.Если что я тебе ничего не говорил)\n",

                     reply_markup=telebot.types.ReplyKeyboardMarkup().add(button_18, button_19,button_20, button_21))

@bot.message_handler(commands=['setting'])
def setting (message):
    global command_type
    command_type = "setting"
    button_18 = telebot.types.KeyboardButton("В городе")
    button_19 = telebot.types.KeyboardButton("В волшебном лесу")
    button_20 = telebot.types.KeyboardButton("В заброшеном задинии")
    button_21 = telebot.types.KeyboardButton("В школе")
    bot.send_message(message.chat.id, text="Выбери сеттинг (локацию где будут главный герой нашего рассказа):\n"
                                           "1) В городе - герой будет гулять по городу...\n"
                                           "2) В волшебном лесу - герой попадет в волшебный лес\n"
                                           "3)В заброшенном здании - герой окажется в заброшенном здании\n"
                                           "4) В школе - наш герой захочет поучиться в школе \n"
                                            ,

                     reply_markup=telebot.types.ReplyKeyboardMarkup().add(button_18, button_19,button_20, button_21))


@bot.message_handler(commands=['do_it'])
def do_it(message):
    bot.send_message(message.chat.id, f"Был выбран такой жанр: {user_genre}")
    bot.send_message(message.chat.id, f"Был выбран такого персонажа: {user_character}")
    bot.send_message(message.chat.id, f"Был выбран такой сеттинг: {user_setting}")
    user_request = (
        f"Напиши текст на русском с жанром {user_genre} с персонажем {user_character} дейсвие происходит {user_setting}.")
    bot.send_message(message.chat.id, f"{user_request}")
    bot.send_message(message.chat.id, text="После того как проверишь напиши /solve_task")
    # записываем выбор данной в базу
    user_id_session = message.from_user.id
    cur = con.cursor()
    query = f'''
                               UPDATE user_story SET setting = "{str(user_setting)}" WHERE user_id = {user_id_session};
                            '''
    print(query)
    cur.execute(query)
    con.commit()
    query = f'SELECT * FROM user_story WHERE user_id = {user_id_session}'
    results = cur.execute(query).fetchone()
    print(results)



@bot.message_handler(commands=['solve_task'])
def solve_task(message):
    global  user_id_session, user_genre, user_character, user_setting,  user_request, command_type
    json = gpt.make_promt(f"Напиши текст на русском с жанром {user_genre} с персонажем {user_character} дейсвие происходит {user_setting}.")
    bot.send_message(message.chat.id, "Ушёл думать...")

    # Отправка запроса
    resp = gpt.send_request(json)

    # Проверяем ответ на наличие ошибок и парсим его
    response = gpt.process_resp(resp)
    if not response[0]:
        bot.send_message(message.chat.id, "Не удалось выполнить запрос...")

        # Выводим ответ или сообщение об ошибке
    bot.send_message(message.chat.id, response[1])
    # записываем ответ данной в базу
    try:
        cur = con.cursor()
        query = f'''
                   UPDATE user_sessions SET gpt_responce = "{str(response[1])}" WHERE user_id = {user_id_session};
                '''
        print(query)
        cur.execute(query)
        con.commit()
    except:
        cur = con.cursor()
        query = f'''
                           UPDATE user_sessions SET gpt_responce = "Ответ от нейросети содержал недопустимые символы" WHERE user_id = {user_id_session};
                        '''
        print(query)
        cur.execute(query)
        con.commit()
    query = f'SELECT * FROM user_sessions WHERE user_id = {user_id_session}'
    results = cur.execute(query).fetchone()
    print(results)
    return


@bot.message_handler(content_types=CONTENT_TYPES)
def mess_engine(message):
    global  user_id_session, user_genre, user_character, user_setting,  user_request, command_type
    # print(command_type)
    if message.content_type != ("text"):
        bot.send_message(message.chat.id, "Необходимо отправить именно текстовое сообщение")
        bot.send_message(message.chat.id,
                         f"Мы остановились на команде /{command_type}. Если решишь продолжжить, просто нажми на команду!")
        return mess_engine
    else:

        if command_type == ("genre"):
            bot.send_message(message.chat.id, "Сейчас мы обрабатываем текст для команды /genre")
            user_genre = message.text
            # user_text = message.text
            bot.send_message(message.chat.id, f"Был выбран такой жанр: {user_genre}")
            print(user_genre)
            bot.send_message(message.chat.id, text="Если определился с жанрм, напиши команду /character")
            command_type = ""
            # записываем выбор данной в базу
            user_id_session = message.from_user.id
            cur = con.cursor()
            query = f'''
               UPDATE user_story SET genre = "{str(user_genre)}" WHERE user_id = {user_id_session};
            '''
            print(query)
            cur.execute(query)
            con.commit()
            query = f'SELECT * FROM user_story WHERE user_id = {user_id_session}'
            results = cur.execute(query).fetchone()
            print(results)

            # cur.execute(f"update user_sessions set items = {str(user_item)} where user_id = {user_id_session}")


        elif command_type == ("character"):
            bot.send_message(message.chat.id, "Сейчас мы обрабатываем текст для команды /character")
            user_character = message.text
            bot.send_message(message.chat.id, f"Был выбран такой жанр: {user_genre}")
            bot.send_message(message.chat.id, f"Был выбран такого персонажа: {user_character}")
            print(user_character)
            bot.send_message(message.chat.id, text="После того как выберешь персонажа напиши /setting")
            command_type = ""

            # записываем выбор данной в базу
            user_id_session = message.from_user.id
            cur = con.cursor()
            query = f'''
                       UPDATE user_story SET character = "{str(user_character)}" WHERE user_id = {user_id_session};
                    '''
            print(query)
            cur.execute(query)
            con.commit()
            query = f'SELECT * FROM user_story WHERE user_id = {user_id_session}'
            results = cur.execute(query).fetchone()
            print(results)

        elif command_type == ("setting"):
            bot.send_message(message.chat.id, "Сейчас мы обрабатываем текст для команды /setting")
            user_setting = message.text
            bot.send_message(message.chat.id, f"Был выбран такой жанр: {user_genre}")
            bot.send_message(message.chat.id, f"Был выбран такого персонажа: {user_character}")
            bot.send_message(message.chat.id, f"Был выбран такой сеттинг: {user_setting}")
            print(user_character)
            bot.send_message(message.chat.id, text="После того как выберешь сложность напиши /do_it")
            command_type = ""

            # записываем выбор данной в базу
            user_id_session = message.from_user.id
            cur = con.cursor()
            query = f'''
                            UPDATE user_story SET setting = "{str(user_setting)}" WHERE user_id = {user_id_session};
                         '''
            print(query)
            cur.execute(query)
            con.commit()
            query = f'SELECT * FROM user_story WHERE user_id = {user_id_session}'
            results = cur.execute(query).fetchone()
            print(results)

        else:
            bot.send_message(message.chat.id, f"Я всегда не против просто поболтать. Буду попугаем: {message.text}")
            bot.send_message(message.chat.id, "Если решишь заставить нейросеть думать за тебя, командуй /genre")

    #cur.close()

# Добавляем айди пользователя


bot.polling()
