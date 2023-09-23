import os
import requests
from urllib.parse import urlparse

from dotenv import load_dotenv


def shorten_link(token, url):
    url_get_bitlink = 'https://api-ssl.bitly.com/v4/bitlinks'
    token_auth = {
     "Authorization": f"Bearer {token}",
    }
    parse = urlparse(url)
    if not parse.scheme:
        url = 'https://' + url

    long_url = {
        "long_url": url,
    }
    response = requests.post(url_get_bitlink,
                             headers=token_auth,
                             json=long_url)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(token, bitlink):
    url_count_click = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'
    token_auth = {
     "Authorization": f"Bearer {token}",
    }
    params = {'units': '-1'}
    parse = urlparse(bitlink)
    if parse.scheme:
        bitlink = parse.netloc + parse.path
    url_for_check = url_count_click.format(bitlink)
    response = requests.get(url_for_check, headers=token_auth, params=params)
    response.raise_for_status()
    click_count = response.json()['total_clicks']
    return click_count


def is_bitlink(token, url):
    url_bitlink_info = 'https://api-ssl.bitly.com/v4/bitlinks/{}'
    parse = urlparse(url)
    if parse.scheme:
        url = parse.netloc + parse.path
    url_for_check = url_bitlink_info.format(url)
    token_auth = {
     "Authorization": f"Bearer {token}",
    }
    response = requests.get(url_for_check, headers=token_auth)
    if response.status_code == 200:
        return True
    else:
        return False


if __name__ == '__main__':

    load_dotenv()

    TOKEN_BITLINK = os.environ['TOKEN_BITLINK']

    url_for_check = input('Ведите ссылку: ')

    if is_bitlink(TOKEN_BITLINK, url_for_check):
        try:
            count_click = count_clicks(token=TOKEN_BITLINK,
                                       bitlink=url_for_check)
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка {error}, попробуйте еще раз')
        print('По вашей ссылке прошли:', count_click, 'раз(а)')
    else:
        try:
            bitlick = shorten_link(TOKEN_BITLINK, url_for_check)
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка {error}, попробуйте еще раз')
        print('Битлинк', bitlick)
