from asyncio.windows_events import NULL
from twocaptcha import TwoCaptcha
from config import API_KEY
from bs4 import BeautifulSoup
import logging, pickle, os, requests

logging.basicConfig(level=logging.DEBUG)


solver = TwoCaptcha(API_KEY)
sitekey = '6Lc3NwoUAAAAALgovRcU2YBbs_EDytbfCEZrK3kh'

url = "https://internetopros.ru/account/login"


def get_cookie(LOGIN_URL):
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    response = requests.get(LOGIN_URL, headers=headers, verify=False)
    return '; '.join([x.name + '=' + x.value for x in response.cookies])

def register(login, password, captcha, __RequestVerificationToken, id_user):
    csrf_token = get_cookie(url)
    
    print('Received CSRF token', csrf_token)
    ReturnUrl = '/private'

    payload = 'ReturnUrl={}&Email={}&Password={}&g-recaptcha-response={}&Captcha={}&__RequestVerificationToken={}'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Referer': f'{url}',
        'Cookie': f'csrftoken={csrf_token}'
    }
    
    mysession = requests.session()


    response = mysession.post(url,
                             headers=headers,
                             data=payload.format(ReturnUrl, login, password, captcha, captcha, __RequestVerificationToken)
                             )

    with open(f"sessions/{id_user}_{login}.pkl", 'wb') as f: 
        pickle.dump(mysession.cookies, f)
    soup = BeautifulSoup(response.text, 'lxml')
    print(response.text)
    print(soup.find("span", {"id": "profile-points__number"}))

def get_cookie_file(letter, lst):
    for word in lst:
        if letter in word:
            return word


def get_session(id_user):
    try:
        sessions = next(os.walk('sessions/'), (None, None, []))[2]
        print('Попытка получения сессии')
        with open(f'sessions/{get_cookie_file(id_user, sessions)}', 'rb') as f: 
            print('Сессия получена')
            return pickle.load(f)
            
    except IOError:
        print('Ошибка присоединения к сессии')
        return 'Ошибка присоединения к сессии. Попробуйте авторизоваться ещё раз'

def get_balance(id_user):
    # Load/Create the session
    session = requests.session()
    session.cookies.update(get_session(id_user))
    print(session.cookies)
    url = 'https://internetopros.ru/private'
    print('Получаем данные сайта')
    response = session.post(url)
    print('Обращаем в объект парсинга')
    soup = BeautifulSoup(response.text, 'lxml')
    if 'Вход' in soup.select('h1.private-page__title')[0].text.strip():
        print('Сессия без авторизации')
        return 'Сессия без авторизации. Повторите попытку входа'
    return soup.find("span", {"id": "profile-points__number"}) or "Проблема с сессией"
    
