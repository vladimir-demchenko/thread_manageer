import time
import random
import threading
from seleniumwire import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import websocket
import json
import asyncio
from datetime import datetime, time as dt_time, timezone, timedelta
import requests

const_cities = {
    '1': {
        'name': 'Moscow',
        'StartField': 25,
        'CurrentField': 0,
        'taken': False,
        'counter': 0
    },
    '1060': {
        'name': 'Sochi',
        'StartField': 15,
        'CurrentField': 0,
        'taken': False,
        'counter': 0
    },
    # "17590": {
    #     "name": "Семаранг",
    #     'StartField': 300,
    #     'CurrentField': 0,
    #     'counter': 0,
    #     'taken': False
    # },
    # "17591": {
    #     "name": "Пхукет",
    #     'StartField': 300,
    #     'CurrentField': 0,
    #     'counter': 0,
    #     'taken': False
    # },
    # "17592": {
    #     "name": "Пекалонган",
    #     'StartField': 300,
    #     'CurrentField': 0,
    #     'counter': 0,
    #     'taken': False
    # },
    # "17593": {
    #     "name": "Денпасар",
    #     'StartField': 300,
    #     'CurrentField': 0,
    #     'counter': 0,
    #     'taken': False
    # },
    # "15552": {
    #     "name": "Бангкок",
    #     'StartField': 300,
    #     'CurrentField': 0,
    #     'counter': 0,
    #     'taken': False
    # },
    # "8809": {
    #     "name": "Дели",
    #     'StartField': 300,
    #     'CurrentField': 0,
    #     'counter': 0,
    #     'taken': False
    # },
    # "8828": {
    #     "name": "Лудхияна",
    #     'StartField': 300,
    #     'CurrentField': 0,
    #     'counter': 0,
    #     'taken': False
    # },
    # "8844": {
    #     "name": "Джакарта",
    #     'StartField': 300,
    #     'CurrentField': 0,
    #     'counter': 0,
    #     'taken': False
    # },
    # "3511": {
    #     "name": "Перт",
    #     'StartField': 300,
    #     'CurrentField': 0,
    #     'counter': 0,
    #     'taken': False
    # },
    "1921": {
        "name": "Екатеринбург",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "2090": {
        "name": "Казань",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "2175": {
        "name": "Томск",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "2272": {
        "name": "Сургут",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "1596": {
        "name": "Владивосток",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "1342": {
        "name": "Нижний Новгород",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "1406": {
        "name": "Новосибирск",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "1287": {
        "name": "Мурманск",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "1042": {
        "name": "Краснодар",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "1116": {
        "name": "Красноярск",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "733": {
        "name": "Иркутск",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "315": {
        "name": "Архангельск",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "173": {
        "name": "Санкт-Петербург",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
}

lock = threading.Lock()


def calculate_new_limit(start_field):
    # Calculate a random percentage between 2% and 5%
    percentage = random.uniform(0.02, 0.05)
    # Randomly choose to increase or decrease the limit
    if random.choice([True, False]):
        return int(start_field * (1 + percentage))
    else:
        return int(start_field * (1 - percentage))


def get_random_city(cities):
    keys = list(cities.keys())

    while True:
        with lock:
            if all(city['taken'] for city in cities.values()):
                return 'All cities are taken'

        random_key = random.choice(keys)

        with lock:
            city = cities[random_key]
            if not city['taken']:
                city['taken'] = True
                return random_key, city


async def send_status(uri, message):
    ws = websocket.create_connection(uri)
    ws.send(message)
    ws.close


def emulate_clicks(city_id, city, proxy):
    start_time = time.time()
    duration = 10 * 60

    chrome_option = Options()
    chrome_option.add_argument('--headless')

    # seleniumwire_option = {
    #     'proxy': {
    #         'http': const_proxies[proxy]['url'],
    #         'verify_ssl': False
    #     }
    # }

    # print(seleniumwire_option)
    # if time.time() - const_proxies[proxy]['when_change'] >= duration:
    #     r_c = requests.get(url=f'https://mobileproxy.space/api.html?command=change_equipment&proxy_id={int(proxy)}&id_city={int(city_id)}',
    #                        headers={'Authorization': 'Bearer f219619fcd8a27b7f8a5167b5426e7dd'})
    #     const_proxies[proxy]['when_change'] = time.time()
    #     response = r_c.json()
    #     if 'error' in response or response['status'] == 'ERR':
    #         return

    while time.time() - start_time < duration:
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=chrome_option) as driver:
            driver.get('http://45.90.218.129/')
            time.sleep(5)
        with lock:
            if city['counter'] < city['StartField']:  # TODO change to CurrField
                city['counter'] += 1
                print(f'Click from {city}')
            if city['counter'] >= city['StartField']:  # TODO change to CurrField
                print('City reached limit')
                break
        message = json.dumps({
            'city': city['name'],
            'clicks': city['counter'],
            'allClicks': city['StartField'],
            'time': datetime.now(timezone(timedelta(hours=3))).isoformat()
        })

        # asyncio.run(send_status('ws://localhost:8000', message))

        # r_ip = requests.get(url=const_proxies[proxy]['change_ip'],
        #                     headers={'User-Agent': 'Chrome/125.0.0.0'})

        # print(r_ip.text)

        time.sleep(random.randint(46, 53))

        if True:  # TODO add cond
            break
    with lock:
        if city['counter'] < city['StartField']:
            city['taken'] = False


def worker():
    while True:
        proxy, proxy_info = get_random_proxy(const_proxies)
        result = get_random_city(const_cities)
        if isinstance(result, str):
            print(result)
            break
        else:
            selected_city_id, selected_city_details = result
            print(f'City id - {selected_city_id}')
            print(f'City details - {selected_city_details}')

        emulate_clicks(selected_city_id, selected_city_details, proxy)

        with proxy_lock:
            if True:  # TODO add cond
                proxy_info['taken'] = False


const_proxies = {
    '264347': {
        'url': 'http://ZEb5Ec:yH5fYn7tEWaK@cproxy.site:12938',
        'when_change': 0,
        'change_ip': 'https://changeip.mobileproxy.space/?proxy_key=980e772781bb8b7a16e451ba936d1564&format=json',
        'taken': False
    },
    '264348': {
        'url': 'http://ut3baE:YnEZmUXrUdgy@yproxy.site:13021',
        'when_change': 0,
        'change_ip': 'https://changeip.mobileproxy.space/?proxy_key=7f5dc59a8d5570d602b37b2699d037fd&format=json',
        'taken': False
    },
    '264344': {
        'url': 'http://TUj9UT:Er9YFeC5udNy@hproxy.site:11084',
        'when_change': 0,
        'change_ip': 'https://changeip.mobileproxy.space/?proxy_key=1cd18878b662fbc4aaab6afd572fb070&format=json',
        'taken': False
    },
    '264345': {
        'url': 'http://GaC6Ca:ZADEDhYW9AN6@wproxy.site:12734',
        'when_change': 0,
        'change_ip': 'https://changeip.mobileproxy.space/?proxy_key=7ab49ecb2fe213c1c19958ed091b5f01&format=json',
        'taken': False
    },
    '264346': {
        'url': 'http://Uh7ymN:CUBmyE6CAk4y@tproxy.site:12917',
        'when_change': 0,
        'change_ip': 'https://changeip.mobileproxy.space/?proxy_key=ddafff33b8fa56e04f8794e1aecfbb92&format=json',
        'taken': False
    },
}


proxy_lock = threading.Lock()


def get_random_proxy(proxies):
    keys = list(proxies.keys())

    while True:
        with proxy_lock:
            if all(proxy['taken'] for proxy in proxies.values()):
                return 'All proxies are taken'

        random_key = random.choice(keys)

        with proxy_lock:
            proxy = proxies[random_key]

            if not proxy['taken']:
                proxy['taken'] = True
                return random_key, proxy


def current_interval():
    now = datetime.now(timezone(timedelta(hours=3)))
    if dt_time(9, 0) <= now.time() < dt_time(17, 0):
        return '09:00-17:00'
    elif dt_time(17, 0) <= now.time() < dt_time(0, 0):
        return '17:00-00:00'
    else:
        return '00:00-09:00'


def manage_threads():
    websocket.enableTrace(True)
    now = datetime.now(timezone(timedelta(hours=3)))
    print(now.isoweekday())

    # proxies = requests.get('http://localhost:8000/proxies')

    # print({item['id']: item for item in proxies.json()})

    threads = []

    for i in range(2):
        t = threading.Thread(target=worker,
                             daemon=True)
        threads.append(t)
        t.start()

    for i in threads:
        i.join()
    # print({item['id']: item for item in test})


if __name__ == '__main__':
    manage_threads()
