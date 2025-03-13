import requests
from bs4 import BeautifulSoup
import time
import datetime

def process_timestamp(time_str):
    return time.strptime(f'{datetime.date.today()} {time_str}', f'%Y-%m-%d %H:%M:%S')

if __name__ == '__main__':
    latest_update = process_timestamp('00:00:00')
    #latest_update = time.localtime()
    print(f'started at {time.strftime("%H:%M:%S", latest_update)}')
    while True:
        time.sleep(10)
        session = requests.Session()
        response = session.request('get', 'https://welt11.freewar.de/freewar/internal/chattext.php')
        if response.status_code != 200:
            print('site not available.')
            session.close()
            continue
        soup = BeautifulSoup(response.text, 'html.parser')
        for chat in soup.find_all('p'):
            timestamp = process_timestamp(chat.span.text)
            if timestamp <= latest_update:
                continue
            chattext = chat.text.replace('  ', ' ')
            print(chattext)
            with open('chattext.log', 'a') as file:
                file.write(f'{chattext}\n')
            latest_update = timestamp
        session.close()
