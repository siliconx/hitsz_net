import re
import time
import random
import hashlib
import requests
import json
import base64
from lxml import etree
from xencode import xencode

home_url = 'http://10.248.98.2/srun_portal_pc?ac_id=1&theme=basic2'
challenge_url = 'http://10.248.98.2/cgi-bin/get_challenge'
login_url = 'http://10.248.98.2/cgi-bin/srun_portal'

username = '19S051022'
password = 'XZB7091wifi'


class HITSZNet(object):
    '''HITSZNet.'''
    def __init__(self):
        super(HITSZNet, self).__init__()
        self.ac_id = '1'
        self.enc = 'srun_bx1'
        self.n = '200'
        self.type = '1'
        self.os = 'Linux'
        self.name = 'Linux'
        self.double_stack = '0'

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
        md5_obj.update(password.encode('utf-8'))
        self.md5_pwd = '{MD5}' + md5_obj.hexdigest()

        data = {
            'username': username,
            'password': password,
            'ip': self.ip,
            'acid': self.ac_id,
            'enc_ver': self.enc
        }
        json_str = json.dumps(data)
        xc = xencode.xEncode(json_str, token)
        self.info = b'{SRBX1}' + base64.b64encode(xc.encode('utf-8'))
        chkstr = token + username
        chkstr += token + self.md5_pwd
        chkstr += token + self.ac_id
        chkstr += token + self.ip
        chkstr += token + self.n
        chkstr += token + self.type
        chkstr = chkstr.encode('utf-8') + token.encode('utf-8') + self.info
        self.chksum = hashlib.sha1(chkstr)

    def login(self):
        '''登陆.'''
        self.get_ip()
        self.gen_callback()
        self.get_challenge()
        self.encryption()

        params = {
            'action': 'login',
            'username': username,
            'password': self.md5_pwd,
            'ac_id': self.ac_id,
            'ip': self.ip,
            'chksum': self.chksum,
            'info': self.info,
            'n': self.n,
            'type': self.type,
            'os': self.os,
            'name': self.name,
            'double_stack': self.double_stack,
            '_': self.timestamp
        }

        r = requests.get(login_url, params=params)
        self.r = r


if __name__ == '__main__':
    if not (username and password):
        username = input('Enter username: ')
        password = input('Enter password: ')
    hit = HITSZNet()
    hit.login()