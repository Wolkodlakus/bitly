import os
import requests
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()

import argparse



token_bit = os.environ['TOKEN_BITLY']

def auth_params(token):
    return {"Authorization" : f"Bearer {token}"}

def shorten_link(token, url="https://google.ru"):

    shortening_url ="https://api-ssl.bitly.com/v4/shorten"

    json_load = {
        "long_url" : url
    }
    
    response = requests.post(shortening_url,json=json_load, headers=auth_params(token))
    response.raise_for_status()
    
    return response.json()["link"]

def count_clicks(token, bitlink):
    counting_url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    
    response = requests.get(counting_url, headers=auth_params(token)) 
    response.raise_for_status()         
    
    return response.json()["total_clicks"]

def is_bitlink(token, url):    
    is_bitlink_url = f"https://api-ssl.bitly.com/v4/bitlinks/{url}"    
    response = requests.get(is_bitlink_url, headers=auth_params(token))        
    
    return response.ok

def main():
    parser = argparse.ArgumentParser(
        description='Скрипт либо создаёт короткие ссылки, либо показывает количество переходов по такой ссылке'
    )
    parser.add_argument('link', help='Ссылка')
    args = parser.parse_args()
    # long_url=input("Введите ссылку: ").strip()
    long_url = args.link
    url_parse = urlparse(long_url)
    short_url = (url_parse.netloc + url_parse.path)
    try:
        if is_bitlink(token_bit,short_url):
            print(f"Всего по этой ссылке перешли {count_clicks(token_bit,short_url)} раз")
        else:
            print("Битлинк", shorten_link(token_bit, long_url))
    except requests.exceptions.HTTPError: 
        print("Ошибка в ссылке")

if __name__ == "__main__":
    main()