import os
import sys
import requests
from urllib.parse import urlparse

from dotenv import load_dotenv


def shorten_link(token, url):
    endpoint = 'https://api-ssl.bitly.com/v4/bitlinks'
    header = {
     "Authorization": f"Bearer {token}",
    }
    long_url = {
        "long_url": url,
    }
    response = requests.post(endpoint,
                             headers=header,
                             json=long_url)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(token, bitlink):
    url = 'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary'
    header = {
     "Authorization": f"Bearer {token}",
    }
    params = {'units': '-1'}
    parts_of_url = urlparse(bitlink)
    bitlink = '{}{}'.format(parts_of_url.netloc, parts_of_url.path)
    formatted_url = url.format(bitlink)
    response = requests.get(formatted_url,
                            headers=header,
                            params=params)
    response.raise_for_status()
    click_count = response.json()['total_clicks']
    return click_count


def is_bitlink(token, url):
    bitlink_info_url = 'https://api-ssl.bitly.com/v4/bitlinks/{}'
    parts_of_url = urlparse(url)
    url = '{}{}'.format(parts_of_url.netloc, parts_of_url.path)
    url_for_check = bitlink_info_url.format(url)
    header = {
     "Authorization": f"Bearer {token}",
    }
    return requests.get(url_for_check, headers=header).ok


def main():
    load_dotenv()

    bitlink_token = os.environ['BITLINK_TOKEN']

    url = input('Ведите ссылку: ')

    if is_bitlink(bitlink_token, url):
        try:
            count_click = count_clicks(token=bitlink_token,
                                       bitlink=url)
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка {error}, попробуйте еще раз')
            sys.exit()
        print('По вашей ссылке прошли:', count_click, 'раз(а)')
    else:
        try:
            bitlick = shorten_link(bitlink_token, url)
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка {error}, попробуйте еще раз')
            sys.exit()
        print('Битлинк', bitlick)


if __name__ == '__main__':
    main()
