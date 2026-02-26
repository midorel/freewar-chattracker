import requests
import random
import websocket
import time
import datetime
import json
from bs4 import BeautifulSoup

#latest_update = time.localtime()

def process_timestamp(time_str):
    return time.strptime(f'{datetime.date.today()} {time_str}', f'%Y-%m-%d %H:%M:%S')

def on_message(ws, message):
    d = json.JSONDecoder()
    raw = d.decode(message)
    try:
        soup = BeautifulSoup(raw['chat'], 'html.parser')
        for chat in soup.find_all('p'):
            # timestamp = process_timestamp(chat.span.text)
            # if timestamp < latest_update:
            #     continue
            # chattext = chat.text.replace('  ', ' ')
            # latest_update = timestamp
            print(chat.text)
    except:
        #print(raw)
        pass

def on_error(ws, error):
    print(f'Error!\n{error}')

def on_close(ws, close_status_code, close_msg):
    print(f'Closed!\n{close_status_code}: {close_msg}')

def on_open(ws):
    print('Opened connection')

if __name__ == '__main__':
    session = requests.session()

    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:131.0) Gecko/20100101 Firefox/131.0',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Site': 'same-origin',
        'DNT': '1',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache',
        'Accept-Language': 'de,en-US;q=0.7,en;q=0.3',
    })

    data = {
        'name': 'name',
        'password': 'passwort',
        'submit': 'Einloggen',
    }

    session.request('post', 'https://welt11.freewar.de/freewar/internal/index.php', data=data)
    session.request('get', 'https://welt11.freewar.de/freewar/internal/friset.php')
    
    session.headers.update({
        'Sec-Fetch-Mode': 'websocket',
        'Sec-WebSocket-Extensions': 'permessage-deflate',
    })

    cookies = f'PHPSESSID="{session.cookies["PHPSESSID"]}"'

    ws = websocket.WebSocketApp(
        'wss://welt11.freewar.de/freewar/internal/ws/3275',
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        cookie=cookies,
    )

    ws.run_forever(
        reconnect=5,
        ping_interval=2,
        ping_payload='ping',
    )
