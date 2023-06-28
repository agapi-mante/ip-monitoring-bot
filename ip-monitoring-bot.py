import requests
from datetime import datetime
import ping3
import time

# Замените значения на свои реальные данные
TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
CHAT_ID = "YOUR_TELEGRAM_CHAT_BOT_TOKEN"

# Список серверов для проверки
servers = {
    'Server 1': 'YOUR_IP_SERVER',
    'Server 2': 'YOUR_IP_SERVER',
    'Server 3': 'YOUR_IP_SERVER'
}

def send_message_to_telegram(msg):  # Отправка сообщения в Telegram
    params = {'chat_id': CHAT_ID, 'text': msg}
    response = requests.get(f'https://api.telegram.org/bot{TOKEN}/sendMessage', params=params)
    if response.status_code != 200:
        print('Ошибка отправки сообщений в Telegram...')

def is_host_alive(host):   # Проверка доступности хоста с помощью ping
    response_time = ping3.ping(host)
    if response_time is not None:
        return True
    return False

def check_server_status(): # Функция для проверки состояния серверов
    status_map = {}
    try:
        while True:
            for server_name, server_ip in servers.items():
                if server_ip not in status_map:
                    status_map[server_ip] = False

                is_alive = is_host_alive(server_ip)

                if is_alive and not status_map[server_ip]:  # Сервер восстановил связь
                    status_map[server_ip] = True
                    message = f'{server_name} ({server_ip}) is up. Date: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}'
                    send_message_to_telegram(message)

                elif not is_alive and status_map[server_ip]: # Сервер потерял связь
                    status_map[server_ip] = False
                    message = f'{server_name} ({server_ip}) is down. Date: {datetime.now().strftime("%d-%m-%Y %H:%M:%S")}'
                    send_message_to_telegram(message)

                time.sleep(5)  # Пауза между проверками состояния серверов
    except KeyboardInterrupt:
        print('Программа завершенна пользователем...')
    except SystemExit:
        print('Обнаружен выход из системы. Остановка программы...')

check_server_status()
