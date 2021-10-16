from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
from getpass import getpass


option = webdriver.ChromeOptions()
option.add_argument('--ignore-certificate-errors')
option.add_argument('--incognito') #membuka web driver dalam mode incognito
option.add_experimental_option('excludeSwitches', ['enable-logging'])
# option.add_argument('--headless') #tanpa membuka window web driver

# user ig yang akan di tarik datanya
user = 'kemenkominfo'

#information for login
username = "your_username"
password = "password"

ig = 'https://www.instagram.com/'
driver = webdriver.Chrome(options=option)
driver.get(f'{ig}accounts/login/')
driver.implicitly_wait(5)

u_input =  driver.find_element(By.CSS_SELECTOR, 'input[name="username"]' )
u_input.send_keys(username)
p_input = driver.find_element(By.CSS_SELECTOR,'input[name="password"]')
p_input.send_keys(password)

b_login = driver.find_element(By.CSS_SELECTOR,'.L3NKy')
b_login.click()

time.sleep(3)
b_login = driver.find_element(By.CSS_SELECTOR,'.yWX7d')
b_login.click()
time.sleep(3)

driver.get(f'{ig}{user}')
time.sleep(3)

# jika ingin scrape data sebanyak jumlah postingannya
num_posts = (driver.find_element(By.CSS_SELECTOR, '.k9GMp .g47SY')).text
num_posts = num_posts.replace(",","")
num_posts = int(num_posts)

posts = driver.find_elements(By.CSS_SELECTOR,'.kIKUG')
coll_posts = []
temp = ''
x = 0
y = 21

##
pop_up = posts[0].find_element(By.CSS_SELECTOR, '._9AhH0')
pop_up.click()
time.sleep(2)

# num_posts dpt diganti n angka, jika hanya ingin mengambil data n postingan
for x in range(num_posts):
    
    x +=1
    print(x)
    
    dict_posts = {'link' : (driver.find_element(By.CSS_SELECTOR, '._2dDPU .k_Q0X a')).get_attribute('href')}
    dict_posts['no'] = x    
    dict_posts['date'] = (driver.find_element(By.CSS_SELECTOR, '._2dDPU .k_Q0X a time')).get_attribute('title')

    # dict_posts['img_link'] = (driver.find_element(By.CSS_SELECTOR, '._2dDPU .KL4Bh')).get_attribute('src')

    
    comments = driver.find_elements(By.CSS_SELECTOR, '.C4VMK')
    coll_comments = []

    for line_comment in comments:
        comment = line_comment.find_elements(By.CSS_SELECTOR, 'span')
        single_comment = {'author' : comment[0].text}
        single_comment['comment'] = comment[1].text
        coll_comments.append(single_comment)

    dict_posts['comments'] = coll_comments
    coll_posts.append(dict_posts)
    if x != 2:
        next_but = driver.find_element(By.CSS_SELECTOR, '._2dDPU ._65Bje ')
        next_but.click()
        time.sleep(4)

with open('output.json', 'w', encoding='utf8') as output:
    json.dump(coll_posts, output,  ensure_ascii=False, indent=4)


driver.close()
driver.quit()
