from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime
import json
import redis


def send_msg(msg):
    global driver
    text_area = driver.find_element_by_css_selector('textarea.cs-textarea')
    text_area.click()
    sleep(1)
    text_area.send_keys(msg)
    text_area.send_keys(Keys.ENTER)
    print('发送弹幕成功！')

room_id = '57321'
url = "https://www.douyu.com/" + room_id

pool = redis.ConnectionPool(host='localhost', port=6379, db=5, decode_responses=True)
r = redis.Redis(connection_pool=pool)


driver = webdriver.Firefox(executable_path=r'C:\Users\ws199\OneDrive\文档\python\geckodriver.exe')
driver.maximize_window()

driver.get(url)
driver.delete_all_cookies()
with open('cookies.json', 'r', encoding='utf-8') as f:
    listCookies = json.loads(f.read())
for cookie in listCookies:
    driver.add_cookie(cookie)

driver.get(url)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pop-zoom-hide'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.firstpay-modal-close'))).click()
sleep(2)
send_msg('.....,')
UL = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'ul.c-list[data-type=chat-list]')))
while True:
    sleep(3)
    item = {'time': '', 'text': ''}
    for li in UL.find_elements_by_tag_name('li'):
        item['time'] = datetime.now().strftime('%y-%m-%d %H:%M')
        item['text'] = li.text
        print(item)
        r.lpush(room_id, item)

    js = 'document.getElementById("js-chat-cont").getElementsByTagName("div")[1].getElementsByTagName("a")[1].click();'

    driver.execute_script(js)







# 初次建立连接，随后方可修改cookie
self.browser.get('http://xxxx.com')
# 删除第一次建立连接时的cookie
self.browser.delete_all_cookies()
# 读取登录时存储到本地的cookie
with open('cookies.json', 'r', encoding='utf-8') as f:
    listCookies = json.loads(f.read())
for cookie in listCookies:
    self.browser.add_cookie({
        'domain': '.xxxx.com',  # 此处xxx.com前，需要带点
        'name': cookie['name'],
        'value': cookie['value'],
        'path': '/',
        'expires': None
    })
# 再次访问页面，便可实现免登陆访问
self.browser.get('http://xxx.com')