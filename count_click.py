import os
import sys
import requests
from urllib.parse import urlparse

from dotenv import load_dotenv


def shorten_link(token, url):
    base_url_for_getting_bitlink = 'https://api-ssl.bitly.com/v4/bitlinks'
    header = {
     "Authorization": f"Bearer {token}",
    }
    long_url = {
        "long_url": url,
    }
    response = requests.post(base_url_for_getting_bitlink,
                             headers=header,
                             json=long_url)
    response.raise_for_status()
    bitlink = response.json()['id']
    return bitlink


def count_clicks(token, bitlink):
    base_url_for_counting_clicks = (
        'https://api-ssl.bitly.com/v4/bitlinks/{}/clicks/summary')
    header = {
     "Authorization": f"Bearer {token}",
    }
    params = {'units': '-1'}
    parts_of_url = urlparse(bitlink)
    bitlink = '{}{}'.format(parts_of_url.netloc, parts_of_url.path)
    bitlink_for_counting_clicks = base_url_for_counting_clicks.format(bitlink)
    response = requests.get(bitlink_for_counting_clicks,
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
    token_auth = {
     "Authorization": f"Bearer {token}",
    }
    response = requests.get(url_for_check, headers=token_auth)
    if response.ok:
        return True
    else:
        return False


def main():
    load_dotenv()

    token_bitlink = os.environ['BITLINK_TOKEN']

    url = input('Ведите ссылку: ')

    if is_bitlink(token_bitlink, url):
        try:
            count_click = count_clicks(token=token_bitlink,
                                       bitlink=url)
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка {error}, попробуйте еще раз')
            sys.exit()
        print('По вашей ссылке прошли:', count_click, 'раз(а)')
    else:
        try:
            bitlick = shorten_link(token_bitlink, url)
        except requests.exceptions.HTTPError as error:
            print(f'Ошибка {error}, попробуйте еще раз')
            sys.exit()
        print('Битлинк', bitlick)


if __name__ == '__main__':
    main()
