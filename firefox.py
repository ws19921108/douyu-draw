from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver import ActionChains
from time import sleep
from datetime import datetime
from bs4 import BeautifulSoup
import redis

room_id = '57321'
url = "https://www.douyu.com/" + room_id

pool = redis.ConnectionPool(host='localhost', port=6379, db=4, decode_responses=True)
r = redis.Redis(connection_pool=pool)


driver = webdriver.Firefox(executable_path=r'C:\Users\ws199\OneDrive\文档\python\geckodriver.exe')
driver.maximize_window()
driver.get(url)

WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pop-zoom-hide'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.firstpay-modal-close'))).click()

while True:
    sleep(3)
    soup = BeautifulSoup(driver.page_source, "html.parser")
    ul = soup.find('ul', attrs={'class': 'c-list', 'data-type': 'chat-list'})
    lis = ul.find_all('li')
    item = {'type': '', 'nickname': '', 'level': '', 'text': '', 'time': ''}
    for li in lis:
        attr_class = li['class']
        if 'hy-chat' in attr_class:
            item['type'] = 1
            item['time'] = datetime.now().strftime('%y-%m-%d %H%M')
            item['level'] = li['data-level']
            item['nickname'] = li.find('span', class_='name').a.string
            item['text'] = li.find('span', class_='chat-msg-item text-cont').string
        r.rpush(room_id, item)

    js = 'document.getElementById("js-chat-cont").getElementsByTagName("div")[1].getElementsByTagName("a")[1].click();'

    driver.execute_script(js)




#
# sleep(10)
# spans = ul.find_elements_by_class_name('chat-msg-item text-cont')
# print(len(spans))
# for span in spans:
#     print(span.text)
#
# ActionChains(driver).move_to_element(btn_clear).click()


