import vk_api, requests, re, time, json, os, shutil, subprocess, sys
from vk_api.longpoll import VkLongPoll, VkEventType
from vktools import Carousel, Element, Text, ButtonColor, OpenLink, Keyboard
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.keyboard import VkKeyboard
import shutil
import os, main
from sys import platform
from requests.adapters import HTTPAdapter

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message})

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

def programmCall(file, id): # Функция для вызова программ, не открывая дополнительную cmd
    print('Запускаем файл')
    if platform == "win32":
        print('Винда')
        subprocess.Popen(['python', file, id, 'argzzz2'])
    elif platform == "linux" or platform == "linux2":
        subprocess.Popen(['python3', f'/home/ubuntu/BotAPI/{file}', id, 'argzzz2'])

# Отправка сообщения
def sender(id, text, keyboard=keyboard2.add_keyboard(), template=None, att=None):
    vk.method('messages.send', {'chat_id' : id, 'message' : text, 'keyboard' : keyboard, 'template' : template, 'random_id' : 0, 'attachment': att})

# ОТПРАВКА СООБЩЕНИЯ ЛС
def sender_private_msg(id, text, keyboard=keyboard2.add_keyboard(), template=None, att=None):
    vk.method('messages.send', {'user_id' : id, 'message' : text, 'keyboard' : keyboard, 'template' : template, 'random_id' : 0, 'attachment': att})

# поиск символа в списке
def find_letter(letter, lst):
    return any(letter in word for word in lst)

# Основной цикл
while True:
    try:
        print('Бот запущен')
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                msg = event.text
                if event.from_chat:
                    id = event.chat_id
                    print('в чат');
                    
                    if '@agent' in msg:
                        msg = msg.partition(' ')[2]
                    print('Сообщение: ', msg)
                    if msg == 'баланс':

                        keyboard = VkKeyboard(inline=True)
                        keyboard.add_button(label = f"Ок")

                        sender(id,  ''.join("Да?"), keyboard=keyboard.get_keyboard())
                    
                    elif msg == "карусель":

                        carousel = {
                            "type": "carousel",
                            "elements": [{
                                    "photo_id": "-206674494_457239035",
                                    "title": "Понедельник",
                                    "description": "Показать расписание на понедельник",
                                    "action": {
                                        "type": "open_photo"
                                    },
                                    "buttons": [{
                                        "action": {
                                            "type": "text",
                                            "label": "пн",
                                            "payload": "{}"
                                        }
                                    }]
                                },
                                {
                                    "photo_id": "-206674494_457239034",
                                    "title": "Вторник",
                                    "description": "Показать расписание на вторник",
                                    "action": {
                                        "type": "open_photo"
                                    },
                                    "buttons": [{
                                        "action": {
                                            "type": "text",
                                            "label": "вт",
                                            "payload": "{}"
                                        }
                                    }]
                                },
                                {
                                    "photo_id": "-206674494_457239037",
                                    "title": "Среда",
                                    "description": "Показать расписание на среду",
                                    "action": {
                                        "type": "open_photo"
                                    },
                                    "buttons": [{
                                        "action": {
                                            "type": "text",
                                            "label": "ср",
                                            "payload": "{}"
                                        }
                                    }]
                                },
                                {
                                    "photo_id": "-206674494_457239039",
                                    "title": "Четверг",
                                    "description": "Показать расписание на четверг",
                                    "action": {
                                        "type": "open_photo"
                                    },
                                    "buttons": [{
                                        "action": {
                                            "type": "text",
                                            "label": "чт",
                                            "payload": "{}"
                                        }
                                    }]
                                },
                                {
                                    "photo_id": "-206674494_457239036",
                                    "title": "Пятница",
                                    "description": "Показать расписание на пятницу",
                                    "action": {
                                        "type": "open_photo"
                                    },
                                    "buttons": [{
                                        "action": {
                                            "type": "text",
                                            "label": "пт",
                                            "payload": "{}"
                                        }
                                    }]
                                },
                                {
                                    "photo_id": "-206674494_457239038",
                                    "title": "Суббота",
                                    "description": "Показать расписание на субботу",
                                    "action": {
                                        "type": "open_photo"
                                    },
                                    "buttons": [{
                                        "action": {
                                            "type": "text",
                                            "label": "сб",
                                            "payload": "{}"
                                        }
                                    }]
                                }
                            ]
                        }
                        carousel = json.dumps(carousel, ensure_ascii=False).encode('utf-8')
                        carousel = str(carousel.decode('utf-8'))

                        sender(id, 'Выберите день недели: ', keyboard=None, template=carousel)

                elif event.from_user:
                    id = event.user_id
                    
                    
                    if msg.lower() == 'баланс':
                        keyboard = VkKeyboard(inline=True)
                        keyboard.add_button(label = f"Ок")

                        sessions = next(os.walk('sessions/'), (None, None, []))[2]

                        if find_letter(str(id), sessions) == True:
                            print('Получение баланса')
                            balance = main.get_balance(str(id))
                            sender_private_msg(id,  ''.join(balance) + ' руб') #, keyboard=keyboard.get_keyboard()
                        else:
                            sender_private_msg(id,  'Ваша сессия не найдена. Используйте команду /start для регистрации')
                        
                    if msg.lower() == '/start':
                        print('Старт')
                        # Советую здесь написать код, чтобы главный файл не реагировал на сообщения,
                        # Пока пользователь использует индивидуальную функцию, например, занести его в игнор лист
                        file = f'login_{id}.py' # Файл индивидуальной работы
                        print('Файл индивид', file)
                        shutil.copyfile('login_example.py', file) # Копируем образец и переносим в файл индивид. работы
                        sender_private_msg(id, 'Регистрация! (на регистрацию отводится 1 минута)\nВведите ваш логин и пароль в формате логин:пароль')	
                        programmCall(file, str(id)) # Запускаем файл индивид. работы
                        time.sleep(60) # Ожидание, чтобы успело получить id
                        print('Время вышло')
                        #os.remove('now id') # Удаляем файл передачи id, так как он больше не нужен, а если его не удалить, то возможно, будет ошибка

                        sessions = next(os.walk('sessions/'), (None, None, []))[2]

                        if find_letter(str(id), sessions) == True:
                            sender_private_msg(id, 'Успешная регистрация!')

                    if msg.lower() == '/run':
                        main.run(str(id))
                        

                        

                        
                   
    except:
        time.sleep(60)
        pass