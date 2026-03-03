import requests
import websocket
import datetime
import json
from bs4 import BeautifulSoup

def on_message(ws, message):
    raw = json.loads(message)
    try:
        soup = BeautifulSoup(raw['chat'], 'html.parser')
        for chat in soup.find_all('p'):
            match chat['class'][0]:
                case 'chattextscream' | 'chattextglobal':
                    log_type = 'chat'
                case 'chattextwhisper' | 'chattextclan' | 'chattextgroup':
                    log_type = 'private'
                case 'chattext' | 'worldsay':
                    log_type = 'field'
                case _:
                    log_type = 'rest'

            with open(f'logs/{log_type}/{datetime.date.today()}.log', 'a') as file:
                if log_type == 'field':
                    chat = chat.text
                
                file.write(f'{chat}\n')

            if log_type == 'chat':
                with open('html/Chattracker.htm', 'r') as file:
                    soup = BeautifulSoup(file.read(), 'html.parser')
                    soup.body.append(chat)
                    new_content = soup.prettify()
                with open('html/Chattracker.htm', 'w') as file:
                    file.write(new_content)

            print(chat)
            
    except:
        with open(f'logs/errors/{datetime.date.today()}.log', 'a') as file:
            file.write(f'{raw}\n')

def on_error(ws, error):
    print(f'Error!\n{error}')
    login_session(ws)

def on_close(ws, close_status_code, close_msg):
    print(f'Closed!\n{close_status_code}: {close_msg}')
    login_session(ws)

def on_reconnect(ws):
    login_session(ws)

def on_open(ws):
    print('Opened connection')

def login_session(ws):
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

    with open("auth/login.json") as file:
        data = json.loads(file.read())
    
    session.request('post', 'https://welt11.freewar.de/freewar/internal/index.php', data=data)
    session.request('get', 'https://welt11.freewar.de/freewar/internal/friset.php')
    
    session.headers.update({
        'Sec-Fetch-Mode': 'websocket',
        'Sec-WebSocket-Extensions': 'permessage-deflate',
    })
    
    ws.cookie = f'PHPSESSID="{session.cookies["PHPSESSID"]}"'


if __name__ == '__main__':
    ws = websocket.WebSocketApp(
        'wss://welt11.freewar.de/freewar/internal/ws/3275',
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
    )

    login_session(ws)

    ws.run_forever(
        reconnect=5,
        ping_interval=2,
        ping_payload='ping',
    )
