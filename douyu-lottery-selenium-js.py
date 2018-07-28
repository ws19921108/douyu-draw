import requests
import json
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from threading import Thread
from queue import Queue
from collections import namedtuple


Filters = ['元', '红包', '现金', '支付宝', 'RMB', 'rmb']
Room = namedtuple('Room', ['room_id', 'stop_time', 'content'])
lottery_code = '302'
base_url = 'https://www.douyu.com/'


def check_lottery_type(room_id):
    info_url = 'https://www.douyu.com/member/lottery/activity_info?room_id=' + room_id
    result = requests.get(info_url).text
    result_json = json.loads(result)
    if 'data' in result_json:
        data = result_json['data']
        status = data['activity_status']
        if status != '4':
            return
        prize_name = data['prize_name']
        if not any(fil in prize_name for fil in Filters):
            return
        join_condition = data['join_condition']
        if 'command_content' not in join_condition:
            return
        stop_time = int(data['start_at']) + join_condition['expire_time']
        content = join_condition['command_content']
        return Room(room_id, stop_time, content)


def get_lottery_rooms(room_q):
    page = 1
    all_url = 'https://www.douyu.com/gapi/rkc/directory/0_0/'

    while True:
        result = requests.get(all_url + str(page)).text
        result_json = json.loads(result)
        data = result_json['data']
        room_list = data['rl']
        for room in room_list:
            icdata = room['icdata']
            if lottery_code in icdata:
                room_id = str(room['rid'])
                res = check_lottery_type(room_id)
                if res:
                    room_q.put(res)
        if page >= data['pgcnt']:
            while not room_q.empty():
                time.sleep(2)
            page = 0
        page += 1
        time.sleep(2)


def run_lottry(room_q):
    # options = Options()
    # options.add_argument('-headless')  # 无头参数
    driver = webdriver.Chrome(
        executable_path=r'C:\Users\ws199\OneDrive\文档\python\chromedriver.exe')  # , chrome_options=options
    driver.set_page_load_timeout(10)
    driver.set_script_timeout(10)
    driver.maximize_window()

    driver.get(base_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'pop-zoom-hide'))).click()
    driver.delete_all_cookies()
    with open('cookies.json', 'r', encoding='utf-8') as f:
        listCookies = json.loads(f.read())
    for cookie in listCookies:
        driver.add_cookie(cookie)
    while True:
        time.sleep(2)
        if not room_q:
            continue
        room = room_q.get()
        if time.time() > room.stop_time:
            continue
        try:
            driver.get(base_url + room.room_id)
            send = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'div.b-btn[data-type=send]')))
            time.sleep(1)
            js1 = '''
            var subs = document.getElementsByTagName("div");
            for(var i = 0; i < subs.length; i++){
                if(subs[i].className == "custom_ld-604e04")
                {
                    subs[i].click();
                }
            }
            '''
            driver.execute_script(js1)
            time.sleep(1)
            js2 = '''
            var buttons = document.getElementsByTagName("button");
            for(var i = 0; i < buttons.length; i++){
                if(buttons[i].className == "b_overBtn-5d8f6b b_overBtn_p-655cbc")
                {
                    buttons[i].click();
                }
        else if(buttons[i].className == "puls_btn-38fb7f")
                {
                    buttons[i].click();
                }
            }
            '''
            driver.execute_script(js2)
            time.sleep(1)
            send.click()
            # WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, 'div.custom_ld-604e04'))).click()
            # time.sleep(1)
            # copy_btn = WebDriverWait(driver, 10).until(
            #     EC.presence_of_element_located((By.CSS_SELECTOR, 'div.custom_ld-604e04')))
            # if copy_btn.text == '复制口令':
            #     copy_btn.click()
            # time.sleep(1)
            # focus_btn = driver.find_elements_by_css_selector('button.puls_btn-38fb7f')
            # if focus_btn:
            #     focus_btn[0].click()
            # time.sleep(1)
            # driver.find_element_by_css_selector('div.b-btn[data-type=send]').click()
            # time.sleep(1)
            # timeout = 10
            # while timeout:
            #     follow_num = driver.find_element_by_css_selector('span[data-anchor-info=nic]').text
            #     if follow_num:
            #         break
            #     time.sleep(2)
            # follow_btn = driver.find_element_by_css_selector('a.r-com-btn[data-anchor-info=follow]')
            # if follow_btn.is_displayed():
            #     follow_btn.click()
            # time.sleep(2)
            # driver.find_element_by_css_selector('button.b_overBtn-5d8f6b').click()
            # time.sleep(2)
            # driver.find_element_by_css_selector('div.b-btn[data-type=send]').click()
        except Exception as e:
            str_e = str(e)
            now = time.strftime('%y-%m-%d %H:%M:%S')
            with open('log.txt', 'a+') as f:
                f.write('{} {}'.format(now, str(e)))


if __name__ == '__main__':
    rooms = Queue()
    p_getting = Thread(target=get_lottery_rooms, args=(rooms,))
    p_running = Thread(target=run_lottry, args=(rooms,))
    p_getting.start()
    p_running.start()
