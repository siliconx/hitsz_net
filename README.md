# 哈工大(深圳)校园网络登陆助手

！注: 适用于无图形化界面的Linux服务器

## 安装步骤

1.下载代码
`git clone git@github.com:siliconx/hitsz_net.git`

2.安装selenium
`pip3 install selenium`

3.下载chrome浏览器

4.下载chrome驱动(https://npm.taobao.org/)
>注意浏览器和驱动的版本应该一致

5.把chrome驱动移动到任一环境变量中的目录，如/usr/local/bin

6.给hitsz_net.py加写权限
`chmod +x hitsz_net.py`

7.把hitsz_net.py移动到任一环境变量中的目录，如/usr/local/bin
>通过以上步骤，就可以通过在命令行输入 `hitsz_net.py` 来登陆校园网络。
