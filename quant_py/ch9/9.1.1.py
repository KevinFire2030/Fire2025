from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup


driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))


url = 'https://www.naver.com/'
driver.get(url)
#driver.page_source[1:1000]


# driver.find_element(By.LINK_TEXT , value = '뉴스').click()


# driver.back()


driver.find_element(By.CLASS_NAME, value = 'search_input').send_keys('퀀트 투자 포트폴리오 만들기')

driver.find_element(By.CLASS_NAME, value = 'btn_search').send_keys(Keys.ENTER)

time.sleep(3)

driver.find_element(By.CLASS_NAME, value = 'box_window').clear()
driver.find_element(By.CLASS_NAME, value = 'box_window').send_keys('이현열 퀀트')
driver.find_element(By.CLASS_NAME, value = 'bt_search').click()


driver.find_element(By.XPATH, value = '//*[@id="lnb"]/div[1]/div/ul/li[2]/a').click()

driver.find_element(By.CLASS_NAME, value = 'option_filter').click()
driver.find_element(By.XPATH, value = '//*[@id="snb"]/div[2]/ul/li[2]/div/div/a[2]').click()

prev_height = driver.execute_script('return document.body.scrollHeight')

while True:
    driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
    time.sleep(2)

    curr_height = driver.execute_script('return document.body.scrollHeight')
    if curr_height == prev_height:
        break
    prev_height = curr_height

html = BeautifulSoup(driver.page_source, 'lxml')
txt = html.find_all(class_ = 'api_txt_lines total_tit _cross_trigger')
txt_list = [i.get_text() for i in txt]


print(txt_list[0:10])


print('ok')