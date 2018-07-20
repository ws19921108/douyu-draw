import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from time import sleep
import json
import redis
from multiprocessing import Process

MAX_ROOM = 10


def get_roomid():
    pool = redis.ConnectionPool(host='localhost', port=6379, db=5, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    while True:
        if r.llen('rand') < MAX_ROOM:
            list_url = 'https://www.douyu.com/member/recommlist/getfreshlistajax?type=2'
            list_text = requests.get(list_url).text
            list_json = json.loads(list_text)

            for room in list_json['room']:
                r.lpush('rand', room['roomid'])
                # rooms.append(room['roomid'])
        sleep(5)


def login_by_cookies(cookies_filename):
    global driver
    room_id = '57321'
    driver.get(base_url+room_id)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pop-zoom-hide'))).click()
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.firstpay-modal-close'))).click()
    driver.delete_all_cookies()
    with open(cookies_filename, 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        driver.add_cookie(cookie)


def enter_room(room_id):
    global driver, base_url, suceed
    try:
        driver.get(base_url + room_id)
        sleep(3)
        # copy_btn = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'button.b_overBtn-5d8f6b')))
        copy_btn = driver.find_element_by_css_selector('button.b_overBtn-5d8f6b')
        if copy_btn and copy_btn.text == u'复制口令':
            copy_btn.click()
            sleep(1)
            try:
                focus_btn = driver.find_element_by_css_selector('button.puls_btn-38fb7f')
                focus_btn.click()
                pass
                sleep(1)
            except Exception as e:
                pass
            driver.find_element_by_css_selector('div.b-btn[data-type=send]').click()
            suceed += 1
            sleep(1)
    except Exception as e:
        pass


if __name__ == "__main__":
    base_url = 'https://www.douyu.com/'
    pool = redis.ConnectionPool(host='localhost', port=6379, db=5, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    r.delete('rand')
    p1 = Process(target=get_roomid)
    p1.start()
    driver = webdriver.Firefox(executable_path=r'C:\Users\ws199\OneDrive\文档\python\geckodriver.exe')
    driver.maximize_window()
    driver.set_page_load_timeout(10)
    login_by_cookies('cookies.json')
    sleep(3)
    while True:
        room = r.lpop('rand')
        enter_room(room)
