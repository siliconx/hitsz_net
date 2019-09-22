#!/usr/bin/python3

# driver download from https://npm.taobao.org/

import time
import getpass
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

def init():
    print('running...')

    home_url = 'http://10.248.98.2/srun_portal_pc?ac_id=1&theme=basic2'
    chrome_options = Options()
    # 解决DevToolsActivePort文件不存在的报错
    chrome_options.add_argument('--no-sandbox')
    # 指定浏览器分辨率
    chrome_options.add_argument('window-size=1920x1080')
    # 谷歌文档提到需要加上这个属性来避免出bug
    chrome_options.add_argument('--disable-gpu')
    # 隐藏滚动条, 应对一些特殊页面
    chrome_options.add_argument('--hide-scrollbars')
    # 不加载图片, 提升加载速度
    chrome_options.add_argument('blink-settings=imagesEnabled=false')
    # 关闭浏览器图形界面, 无GUI的操作系统不加这条会启动失败
    chrome_options.add_argument('--headless')

    global driver
    driver = webdriver.Chrome(options=chrome_options)
    driver.get(home_url)
    # 等待页面加载
    time.sleep(1)

    # 获取用户名输入框
    username_input = driver.find_element_by_id('username')
    # 获取密码输入框
    pwd_input = driver.find_element_by_id('password')
    # 填入用户名和密码
    username_input.send_keys(username)
    pwd_input.send_keys(password)


def login():
    '''登陆.'''
    # 登陆按钮
    button = driver.find_element_by_id('login')
    button.click()
    # 等待页面加载
    time.sleep(1)

    page = driver.page_source
    if '帐户余额' in page:
        msg = 'login success'
    elif '已经在线了' in page:
        msg = 'already online'
    elif '用户不存在' in page:
        msg = 'user not exist'
    elif '帐号或密码错误' in page:
        msg = 'username or password error'
    else:
        msg = 'something wrong, try again later'
    print(msg)

def logout():
    '''注销.'''
    # 注销按钮
    button = driver.find_element_by_id('logout-dm')
    button.click()
    # 等待页面加载
    time.sleep(1)

    page = driver.page_source
    if 'DM下线成功' in page:
        msg = 'logout success'
    elif '当前设备不在线' in page:
        msg = 'already offline'
    elif 'SomeParameterError' in page:
        msg = 'some parameter error'
    else:
        msg = 'something wrong, try again later'
    print(msg)

if __name__ == '__main__':
    # 可直接填入账号密码，免输入登陆注销
    username = ''
    password = ''
    if not (username and password):
        username = input('Enter username: ')
        password = getpass.getpass('Enter password: ')

    init()
    action = input('1-login\n2-logout\n')
    if action == '1':
        login()
    else:
        logout()

driver.close()
