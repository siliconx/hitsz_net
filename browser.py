# driver download from https://npm.taobao.org/

from selenium import webdriver

home_url = 'http://10.248.98.2/srun_portal_pc?ac_id=1&theme=basic2'
driver = webdriver.Chrome()

driver.get(home_url)
un_input = driver.find_element_by_id('username')
pwd_input = driver.find_element_by_id('password')
button = driver.find_element_by_id('login')

un_input.send_keys('19S051022')
pwd_input.send_keys('XZB7091wifi')
button.click()