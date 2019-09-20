import requests
from lxml import etree

home = 'http://10.248.98.2/srun_portal_pc?ac_id=1&theme=basic2'

def ip():
	'''获取ip地址.'''
	# 下载页面
	r = requests.get(home)
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
