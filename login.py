import requests
from lxml import etree

home_url = 'http://10.248.98.2/srun_portal_pc?ac_id=1&theme=basic2'
login_url = 'http://10.248.98.2/cgi-bin/get_challenge?callback=jQuery1124077608628830025_1568990931543&username=19S051022&ip=10.249.73.17&_=1568990931544'

def ip():
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

    return ip
