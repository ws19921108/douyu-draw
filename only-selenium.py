from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys

from time import sleep
from datetime import datetime

import redis


def send_msg(msg):
    global driver
    text_area = driver.find_element_by_css_selector('textarea.cs-textarea')
    text_area.click()
    sleep(1)
    text_area.send_keys(msg)
    text_area.send_keys(Keys.ENTER)
    print('发送弹幕成功！')


qq_user = '467044064'
qq_pass = '*********'
login_url = 'https://passport.douyu.com/member/login'
room_id = '57321'
url = "https://www.douyu.com/" + room_id

pool = redis.ConnectionPool(host='localhost', port=6379, db=5, decode_responses=True)
r = redis.Redis(connection_pool=pool)


driver = webdriver.Firefox(executable_path=r'C:\Users\ws199\OneDrive\文档\python\geckodriver.exe')
driver.maximize_window()

driver.get(url)
old_handle = driver.current_window_handle
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pop-zoom-hide'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.firstpay-modal-close'))).click()
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.u-login'))).click()
sleep(1)
driver.switch_to.frame('login-passport-frame')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-type=login]'))).click()
sleep(1)
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'a.third-icon-qq'))).click()
sleep(1)
login_window = driver.window_handles[-1]
driver.switch_to.window(login_window)
sleep(1)
driver.switch_to.frame(0)
sleep(1)
login_href = driver.find_element_by_css_selector('a#switcher_plogin')
login_href.click()
sleep(1)
input_user = driver.find_element_by_css_selector('input#u')
input_user.click()
input_user.send_keys(qq_user)
input_pass = driver.find_element_by_css_selector('input#p')
input_pass.click()
input_pass.send_keys(qq_pass)
input_btn = driver.find_element_by_css_selector('input#login_button')
input_btn.click()
sleep(1)
new_hanle = driver.current_window_handle
driver.switch_to.window(old_handle)
driver.close()
driver.switch_to.window(new_hanle)
sleep(1)
driver.switch_to.frame(0)
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



