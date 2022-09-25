# coding=utf-8

### файл индивидуальноый работы ###
import vk_api, requests, re, time, json, os, shutil, sys, main
import shutil
import time
import os
import vk_api, json
from vk_api.longpoll import VkLongPoll, VkEventType
from vktools import Carousel, Element, Text, ButtonColor, OpenLink, Keyboard
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard

# API-ключ созданный ранее
token = "72271767a6da89d5b1d037f45982439eb0ccbd5264f784156fbc8d1a9d9a9159940481fb54ebe4440f9fa"

# Авторизуемся как сообщество
vk = vk_api.VkApi(token=token)

# Клавиатура
keyboard2 = Keyboard(
    [
        [
            Text("Вывод"),
            Text("Баланс", ButtonColor.PRIMARY)
        ],
        [
            OpenLink("🕸️Сайт", "https://internetopros.ru/private")
        ]
    ]
)

# Работа с сообщениями
longpoll = VkLongPoll(vk)

# Отправка сообщения
def sender(id, text, keyboard=keyboard2.add_keyboard(), template=None, att=None):
    vk.method('messages.send', {'chat_id' : id, 'message' : text, 'keyboard' : keyboard, 'template' : template, 'random_id' : 0, 'attachment': att})

# ОТПРАВКА СООБЩЕНИЯ ЛС
def sender_private_msg(id, text, keyboard=keyboard2.add_keyboard(), template=None, att=None):
    vk.method('messages.send', {'user_id' : id, 'message' : text, 'keyboard' : keyboard, 'template' : template, 'random_id' : 0, 'attachment': att})

# Здесь такой же импорт модулей и установка бота
print(f"Инициализация в файле {os.path.basename(sys.argv[0])} прошла успешно. Передан аргумент", sys.argv[1])
id = int(sys.argv[1])
meFile = f'login_{str(id)}.py'

# Основной цикл
while True:
    try:
        print('Бот запущен')
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                msg = event.text

                if event.from_user:
                    new_id = event.user_id # Получаем новый id
                    if new_id == id: # Если нам написал тот же пользователь
                        print('id совпало')
                        msg = event.text

                        if '@bot_talker' in msg.lower():
                            msg = msg.partition(' ')[2]
                        
                        if '@' in msg:
                            data_login = msg.split(':')
                            print('логин:', data_login[0])
                            print('пароль:', data_login[1])
                        else:
                            data_captcha = msg.split(':')
                            print('капча:', data_captcha[0])
                            print('токен:', data_captcha[1])

                        if '@' in msg.split(':')[0] and len(data_login) == 2:
                            sender_private_msg(id, 'Отлично! Теперь проверим являетесь ли вы человеком \nВведите хеш капчи и токен капчи в формате хеш:токен')
                        
                        if not '@' in msg and len(data_login) != 0:
                            sender_private_msg(id, 'Вроде всё верно \nРегистрируемся...')
                            main.register(data_login[0], data_login[1], data_captcha[0], data_captcha[1], id)
                            os.remove(meFile)
                            break


                        os.remove(meFile) # Удалить себя
                        break #break всё равно придётся написать, так как если запущен цикл, код не перестаёт работать, пока не прекратиться цикл, даже если файл с кодом удалён
                        

    except:
        time.sleep(60)
        pass