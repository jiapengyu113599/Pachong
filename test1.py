import requests
from bs4 import BeautifulSoup
import re
import json
import os

def getHtml(baseurl):
    head = {    #模拟浏览器身份头向对方发送消息
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.56 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.56"
    }
    try:
        response = requests.get(url = baseurl, headers = head)
        if response.status_code==200:
            return response.content.decode("utf-8")
    except:
        print("请求失败")

def main():
    print("这是bv号弹幕获取软件")
    bv = input("请输入bv号: ")
    p = int(input("请输入p号: "))
    baseurl = "https://www.bilibili.com/video/BV"+str(bv)+"?p="+str(p)
    # 获取网页的源代码
    req=getHtml(baseurl)
    # cid所在的位置是window.__INITIAL_STATE__={}里面，所以要在这里找各个cid号
    pattern = r'\<script\>window\.__INITIAL_STATE__=(.*?)\</script\>'
    # result结果得是string
    result = re.findall(pattern, req)[0]
    match_rule = r'{"cid":(.*?),'
    cid = re.findall(match_rule, result)
    # 打开弹幕资源位置
    baseurl = "https://api.bilibili.com/x/v1/dm/list.so?oid="+str(cid[p-1])
    req = getHtml(baseurl)
    soup = BeautifulSoup(req,'html.parser')
    match_rule = r'<d p=".*">(.*?)</d>'
    cid = ""
    for item in soup.find_all('d'):
        item = str(item)
        danmu = re.findall(match_rule, item)[0]
        cid = cid + danmu + " "
    print(cid)
    os.system("pause")

if __name__ == "__main__":
    main()
