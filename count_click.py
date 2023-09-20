import os
import requests
from urllib.parse import urlparse

from dotenv import load_dotenv


load_dotenv()


TOKEN = os.getenv('TOKEN')


token = {
    "Authorization": f"Bearer {TOKEN}",
}
url_get_bitlink = 'https://api-ssl.bitly.com/v4/bitlinks'
url_count_click = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'
params = {'units': '-1'}


def get_shorten_link(token, url):
    json = {
        "long_url": url,
    }
    response = requests.post(url, headers=token, json=json)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def check_count_clicks(token, url, bitlink):
    url_template = url.format(bitlink)
    response = requests.get(url_template, headers=token, params=params)
    response.raise_for_status()
    count_click = response.json()['total_clicks']
    return count_click


def is_bitlink(*args):
    global url
    global bitlink
    url_for_check = input('Ведите ссылку: ')
    parsed = urlparse(url_for_check)
    if parsed.scheme:
        url = url_for_check
        return False
    else:
        bitlink = url_for_check
        return True


if __name__ == '__main__':
    if is_bitlink():
        try:
            count_click = check_count_clicks(token=token,
                                             url=url_count_click,
                                             bitlink=bitlink)
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка {error}, попробуйте еще раз')
        print('По вашей ссылке прошли:', count_click, 'раз(а)')
    else:
        try:
            bitlick = get_shorten_link(token, url_get_bitlink)
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка {error}, попробуйте еще раз')
        print('Битлинк', bitlick)
