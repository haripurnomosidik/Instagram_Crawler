from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json

option = webdriver.ChromeOptions()
option.add_argument('--ignore-certificate-errors')
option.add_argument('--incognito') #membuka web driver dalam mode incognito
option.add_experimental_option('excludeSwitches', ['enable-logging'])
# option.add_argument('--headless') #tanpa membuka window web driver

user = 'ig_user_to_scrape'
ig = 'https://www.instagram.com/'
driver = webdriver.Chrome(options=option)
driver.get(f'{ig}accounts/login/')
driver.implicitly_wait(5)

u_input =  driver.find_element(By.CSS_SELECTOR, 'input[name="username"]' )
u_input.send_keys('your_username')
p_input = driver.find_element(By.CSS_SELECTOR,'input[name="password"]')
p_input.send_keys('your_pass')

b_login = driver.find_element(By.CSS_SELECTOR,'.L3NKy')
b_login.click()

time.sleep(3)
b_login = driver.find_element(By.CSS_SELECTOR,'.yWX7d')
b_login.click()
time.sleep(3)

driver.get(f'{ig}{user}')
time.sleep(3)
posts = driver.find_elements(By.CSS_SELECTOR,'.kIKUG')
coll_posts = []
temp = ''
x = 0
y = 21

##
pop_up = posts[0].find_element(By.CSS_SELECTOR, '._9AhH0')
pop_up.click()
time.sleep(2)


for x in range(42):
    # if temp != post.get_attribute('href')
    # if n == y:
    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
    #     time.sleep(3)
    #     y += 9
    x +=1
    print(x)
    # pop_up close
    # pop_up = post.find_element(By.CSS_SELECTOR, '._9AhH0')
    # pop_up.click()
    # time.sleep(2)
    # webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    # time.sleep(2)

    
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
    if x != 41:
        next_but = driver.find_element(By.CSS_SELECTOR, '._2dDPU ._65Bje ')
        next_but.click()
        time.sleep(3)

with open('output.json', 'w', encoding='utf8') as output:
    json.dump(coll_posts, output,  ensure_ascii=False, indent=4)


# # driver.close()
# # driver.quit()
