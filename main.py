import argparse
import logging
import os
from urllib.parse import urlsplit

import requests
from dotenv import load_dotenv


def shorten_link(token, link):
    url = 'https://api-ssl.bitly.com/v4/bitlinks'
    headers = {"Authorization": f"Bearer {token}"}
    payload = {"long_url": link}
    
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    
    bitlink = response.json()['link']
    return bitlink


def count_clicks(token, url_without_scheme):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{url_without_scheme}/clicks/summary'
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    
    clicks_count = response.json()['total_clicks']
    return clicks_count


def is_bitlink(url_without_scheme, token):
    url = f'https://api-ssl.bitly.com/v4/bitlinks/{url_without_scheme}'
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.get(url, headers=headers)
    
    return response.ok


def main():
    load_dotenv()
    bitly_token = os.getenv('BITLY_TOKEN')

    parser = argparse.ArgumentParser(description='Программа создает битлинк')
    parser.add_argument("link", help="Укажите здесь ссылку на сайт:")
    args = parser.parse_args()
    link = args.link

    parsed_url = urlsplit(link)
    url_without_scheme = f'{parsed_url.netloc}{parsed_url.path}'
    
    try:
        if is_bitlink(url_without_scheme, bitly_token):
            clicks_count = count_clicks(bitly_token, url_without_scheme)
            print("Количество переходов по ссылке битли:",clicks_count)
        else:
            bitlink = shorten_link(bitly_token, link)
            print('Битлинк', bitlink)
    except requests.exceptions.HTTPError:
        logging.warning("Вы ввели не существующую ссылку!")


if __name__ == '__main__':
    main()
