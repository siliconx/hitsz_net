import re
import time
import random
import hashlib
import requests
import json
from lxml import etree

home_url = 'http://10.248.98.2/srun_portal_pc?ac_id=1&theme=basic2'
challenge_url = 'http://10.248.98.2/cgi-bin/get_challenge'
login_url = 'http://10.248.98.2/cgi-bin/srun_portal'

username = '19S051022'
password = 'XZB7091wifi'


class HITSZNet(object):
    '''HITSZNet.'''
    def __init__(self):
        super(HITSZNet, self).__init__()

    def get_ip(self):
        '''获取ip地址.'''
        # 下载页面
        r = requests.get(home_url)
        # 解析html
        html = etree.HTML(r.text)
        # 定位id为user_ip的<input>标签
        ip_tag = html.xpath('//input[@id="user_ip"]')
        if ip_tag:
            # 提取ip地址
            ip = ip_tag[0].attrib['value']
        else:
            ip = None

        self.ip = ip

    def gen_callback(self):
        '''生成callback参数.'''
        # 21位随机数
        rand_num = '11240'
        rand_num += ''.join(random.sample('0123456789', 8)) * 2
        # 时间戳
        timestamp = '%d' % int(time.time() * 1000)
        self.callback = 'jQuery' + rand_num + '_' + timestamp
        self.timestamp = timestamp

    def get_challenge(self):
        '''获取`challenge`.'''
        # 参数
        params = {
            'callback': self.callback,
            'username': username,
            'ip': self.ip,
            '_': self.timestamp
        }
        # 获取响应
        r = requests.get(challenge_url, params=params)
        # 正则匹配
        re_obj = re.search(r'{.*}', r.text)
        # 提取有效json字符串
        extract = re_obj.group(0)
        # 解析json字符串
        data = json.loads(extract)
        self.challenge = data.get('challenge')

    def encryption(self):
        '''加密.'''
        token = self.challenge
        md5_obj = hashlib.md5(token.encode('utf-8'))
        obj.update(password.encode('utf-8'))
        self.pwd = '{MD5}' + obj.hexdigest()


    def login(self):
        '''登陆.'''
        self.get_ip()
        self.gen_callback()
        self.get_challenge()

        params = {
            'action': 'login',
            'username': username,
            'password': password,
            'ac_id': '1',
            'ip': self.ip,
            #'chksum': chksum(chkstr),
            #'info': info,
            'n': '200',
            'type': '1',
            'os': 'Linux',
            'name': 'Linux',
            'double_stack': '0',
            '_': self.timestamp
        }


if __name__ == '__main__':
    if not (username and password):
        username = input('Enter username: ')
        password = input('Enter password: ')
    hit = HITSZNet()
    hit.login()