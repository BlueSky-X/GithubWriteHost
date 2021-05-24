"""
说明：
    1. 通过访问 https://github.com.ipaddress.com/ 获取Github的最佳ip
    2. 将ip写入到hosts文件中
    3. 执行刷新DNS缓存
参考：
    1. bs4如何使用： https://www.cnblogs.com/gl1573/p/9480022.html

"""
from __future__ import print_function

from sys import executable
from requests import get
from os import system
from bs4 import BeautifulSoup
import json
from ctypes import windll


def is_admin():
    try:
        return windll.shell32.IsUserAnAdmin()
    except:
        return False


def GetIP():
    try:
        r = get(url)
    except:
        print("爬取失败,请检查网络连接")

    demo = r.text
    soup = BeautifulSoup(demo, "html.parser")
    tag = soup.find_all("script")[5].string
    tag_json = json.loads(tag)
    ip_text = tag_json['mainEntity'][-3]['acceptedAnswer']['text']
    BestIP = ip_text[94:106]
    print("IP爬取成功，最佳IP为: ", BestIP)
    return BestIP


def writeHosts():
    data = ""
    flag = 0
    with open(PATH, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if (hosts_webdress in line) and (line.startswith('#') == 0):
                flag = 1
                newLine = ip + ' ' + hosts_webdress + '\n'
                data += newLine
            else:
                data += line
    if flag == 0:
        line = ip + ' ' + hosts_webdress
        data += line
        etc = "199.232.69.194 https://github.global.ssl.fastly.net\n \
            185.199.108.153 assets-cdn.github.com\n \
            185.199.109.153 assets-cdn.github.com\n \
            185.199.110.153 assets-cdn.github.\n \
            185.199.111.153 assets-cdn.github.com\n"
        data += etc
    with open(PATH, 'r+') as f1:
        f1.writelines(data)
    print("写入成功")


if __name__ == "__main__":
    url = "https://github.com.ipaddress.com/"
    PATH = r"C:\Windows\System32\drivers\etc\hosts"
    command = "ipconfig /flushdns"
    hosts_webdress = "https://github.com"
    # 获取管理员权限
    if is_admin():
        # 获取ip
        ip = GetIP()
        # 写入hosts文件
        writeHosts()
        # 刷新DNS
        system(command)
        system("pause")
    else:
        windll.shell32.ShellExecuteW(None, "runas", executable, __file__, None, 1)
