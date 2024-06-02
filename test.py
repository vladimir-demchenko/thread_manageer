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
from const import click_config

API_URL = 'http://localhost:8000'

const_cities = {
    '1': {
        'name': 'Москва',
        'StartField': 0,
        'CurrentField': 0,
        'taken': False,
        'counter': 0
    },
    '1060': {
        'name': 'Сочи',
        'StartField': 15,
        'CurrentField': 0,
        'taken': False,
        'counter': 0
    },
    "17590": {
        "name": "Семаранг",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "17591": {
        "name": "Пхукет",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "17592": {
        "name": "Пекалонган",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "17593": {
        "name": "Денпасар",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "15552": {
        "name": "Бангкок",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "8809": {
        "name": "Дели",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "8828": {
        "name": "Лудхияна",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "8844": {
        "name": "Джакарта",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "3511": {
        "name": "Перт",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
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
    "14031": {
        "name": "Майами",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "14149": {
        "name": "Чикаго",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False

    },
    "14670": {
        "name": "Нью-Йорк",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "15084": {
        "name": "Филадельфия",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "15186": {
        "name": "Хьюстон",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "12144": {
        "name": "Амстердам",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "12204": {
        "name": "Утрехт",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "12233": {
        "name": "Делфт",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "12814": {
        "name": "Краков",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "12816": {
        "name": "Варшава",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "13112": {
        "name": "Лиссабон",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "15939": {
        "name": "Хельсинки",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "16130": {
        "name": "Ницца",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "16492": {
        "name": "Париж",
        'StartField': 300,
        'CurrentField': 0,
        'counter': 0,
        'taken': False
    },
    "16675": {
        "name": "Прага",
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

        with lock:
            if all(city['counter'] >= city['StartField'] for city in cities.values()):
                return 'No available city'

        random_key = random.choice(keys)

        with lock:
            city = cities[random_key]
            if not city['taken'] and city['counter'] < city['StartField']:
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

    seleniumwire_option = {
        'proxy': {
            'http': const_proxies[proxy]['url'],
            'verify_ssl': False
        }
    }

    print(seleniumwire_option)
    if time.time() - const_proxies[proxy]['when_change'] >= duration:
        r_c = requests.get(url=f'https://mobileproxy.space/api.html?command=change_equipment&proxy_id={int(proxy)}&id_city={int(city_id)}',
                           headers={'Authorization': f"Bearer {config['api_key']}"})
        const_proxies[proxy]['when_change'] = time.time()
        response = r_c.json()
        if 'error' in response or response['status'] == 'ERR':
            return

    while time.time() - start_time < duration:
        if check_pause_flag():
            time.sleep(1)
            continue
        with webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), chrome_options=chrome_option) as driver:
            driver.get(config['url'])
            time.sleep(5)
        with lock:
            if city['counter'] < city['CurrentField']:  # TODO change to CurrField
                city['counter'] += 1
                print(f'Click from {city}')
            if city['counter'] >= city['CurrentField']:  # TODO change to CurrField
                print('City reached limit')
                break
        message = json.dumps({
            'city': city['name'],
            'clicks': city['counter'],
            'allClicks': city['CurrentField'],
            'time': datetime.now(timezone(timedelta(hours=3))).isoformat()
        })

        asyncio.run(send_status('ws://localhost:8000', message))

        r_ip = requests.get(url=const_proxies[proxy]['change_ip'],
                            headers={'User-Agent': 'Chrome/125.0.0.0'})

        print(r_ip.text)
        current_config = current_interval_config()
        time.sleep(random.randint(
            interval_config[current_config]['delayFrom'], interval_config[current_config]['delayTo']))

    with lock:
        if city['counter'] < city['StartField']:
            city['taken'] = False


def worker():
    proxy_result = get_random_proxy(const_proxies)
    while True:
        if check_pause_flag():
            time.sleep(1)
            continue
        result = get_random_city(const_cities)
        if isinstance(result, str):
            print(result)
            break
        if isinstance(proxy_result, str):
            print(proxy_result)
            break
        else:
            selected_city_id, selected_city_details = result
            proxy, proxy_info = proxy_result
            print(f'City id - {selected_city_id}')
            print(f'City details - {selected_city_details}')

        emulate_clicks(selected_city_id, selected_city_details, proxy)


const_proxies = {}


def check_pause_flag():
    response = requests.get(f"{API_URL}/config")
    data = response.json()
    return data['pause']


def all_proxies():
    response = requests.get(f"{API_URL}/proxies")
    data = response.json()
    return {item['id']: item for item in data}


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


def reset_cities(cities):
    with lock:
        for city in cities.values():
            city['taken'] = False
            city['counter'] = 0


def current_interval_config():
    now = datetime.now(timezone(timedelta(hours=3)))
    if dt_time(9, 0) <= now.time() < dt_time(17, 0):
        return '09:00-17:00'
    elif dt_time(17, 0) <= now.time() < dt_time(0, 0):
        if 4 <= now.isoweekday() <= 6:
            return '17:00-00 inc'
        else:
            return '17:00-00:00'
    elif dt_time(0, 0) <= now.time() < dt_time(3, 0):
        if 5 <= now.isoweekday() <= 7:
            return '00:00-03:00 inc'
        else:
            return '00:00-03:00'
    else:
        if 5 <= now.isoweekday() <= 7:
            return '03:00-09:00 inc'
        else:
            return '03:00-09:00'


def update_start_field(cities, config, current_interval_config):
    with lock:
        for city_id, new_value in config.items():
            if city_id in cities:
                cities[city_id]['StartField'] = current_interval_config['amountOfClicks'] * new_value
                cities[city_id]['CurrentField'] = calculate_new_limit(
                    cities[city_id]['StartField'])


def get_all_clicks(cities):
    count = 0
    allTarget = 0
    for city in cities.values():
        count += city['counter']
        allTarget += city['CurrentField']
    return count, allTarget


config = {}


def get_config():
    response = requests.get(API_URL+'/config')
    return response.json()


interval_config = {
    '09:00-17:00': {
        'threads': 2,
        'amountOfClicks': 450,
        'delayFrom': 60,
        'delayTo': 180
    },
    '17:00-00:00': {
        'threads': 5,
        'amountOfClicks': 1800,
        'delayFrom': 67,
        'delayTo': 74
    },
    '17:00-00:00 inc': {
        'threads': 5,
        'amountOfClicks': 2500,
        'delayFrom': 48,
        'delayTo': 53
    },
    '00:00-03:00': {
        'threads': 2,
        'amountOfClicks': 240,
        'delayFrom': 85,
        'delayTo': 93
    },
    '03:00-09:00': {
        'threads': 2,
        'amountOfClicks': 160,
        'delayFrom': 257,
        'delayTo': 284
    },
    '00:00-03:00 inc': {
        'threads': 2,
        'amountOfClicks': 420,
        'delayFrom': 49,
        'delayTo': 54
    },
    '03:00-09:00 inc': {
        'threads': 2,
        'amountOfClicks': 280,
        'delayFrom': 146,
        'delayTo': 162
    },
}


def manage_threads():

    websocket.enableTrace(True)

    active_threads = []
    previous_interval = None

    while True:
        if check_pause_flag():
            time.sleep(1)
            continue

        global config
        config = get_config()

        with proxy_lock:
            global const_proxies
            const_proxies = all_proxies()

        interval = current_interval()
        current_config = current_interval_config()

        if interval != previous_interval:
            reset_cities(const_cities)
            update_start_field(
                const_cities, click_config[interval], interval_config[current_config])
            previous_interval = interval

        now = datetime.now(timezone(timedelta(hours=3)))
        if now.time() == dt_time(19, 0):
            update_start_field(
                const_cities, click_config["19:00"], interval_config[current_config])
        if now.time() == dt_time(21, 0):
            update_start_field(
                const_cities, click_config["21:00"], interval_config[current_config])

        desired_count = interval_config[current_config]['threads']

        # Add threads if there are less than the desired count
        while len(active_threads) < desired_count:
            t = threading.Thread(
                target=worker, name=f"Worker-{len(active_threads)+1}")
            t.start()
            active_threads.append(t)

        # Remove threads if there are more than the desired count
        while len(active_threads) > desired_count:
            thread_to_stop = active_threads.pop()
            thread_to_stop.join()

        time.sleep(30)


if __name__ == '__main__':
    manage_threads()
