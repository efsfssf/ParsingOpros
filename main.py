from asyncio.windows_events import NULL
import requests
from twocaptcha import TwoCaptcha
from config import API_KEY
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.DEBUG)


solver = TwoCaptcha(API_KEY)
sitekey = '6Lc3NwoUAAAAALgovRcU2YBbs_EDytbfCEZrK3kh'

url = "https://internetopros.ru/account/login"
mysession = NULL
soup = NULL


def get_cookie(LOGIN_URL):
    headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
    }
    response = requests.get(LOGIN_URL, headers=headers, verify=False)
    return '; '.join([x.name + '=' + x.value for x in response.cookies])

def main(login, password, captcha, __RequestVerificationToken):
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
    soup = BeautifulSoup(response.text, 'lxml')
    
