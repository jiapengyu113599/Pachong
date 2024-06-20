import requests
from bs4 import BeautifulSoup
import matplotlib
from matplotlib import pyplot as plt
import jieba
import wordcloud
import pandas as pd
import snownlp
from snownlp import SnowNLP
import seaborn as sn

url="https://comment.bilibili.com/1251331073.xml"
response = requests.get(url) #要爬取的网址
response.encoding='utf-8'
html = response.text
soup = BeautifulSoup(html,"xml") #使用beautifulsoup库快速查找我们想要的信息
all_txt = soup.findAll("d") #寻找到所有包含d的行
txt=[all_txts.attrs ["p"]for all_txts in all_txt] #寻找到所有包含d的行中属性为p的值，这里边包含了弹幕的虚拟id等
txtss=[all_txts.string for all_txts in all_txt] #寻找到所有包含d的行中的字符串数据，即弹幕内容
txtsss=[txts.replace(' ','') for txts in txtss] #将字符串中的空格消除掉
print(txt,txtsss) ###打印便可看见一条条弹幕的属性和内容了。



danmustr=''.join(i for i in txtsss) #将所有弹幕拼接在一起
words=list(jieba.cut(danmustr))  ###利用jieba库将弹幕按词进行切分
words=[i for i in words if len(i)>1] ###挑出长度大于1的词语（为去除诸如？，哈，啊等字符）
wc=wordcloud.WordCloud(height=1000,width=1000,font_path='simsun.ttc')#利用wordcloud库定义词云图片的信息
wc.generate(' '.join(words))   ##生成图片
print(wc)
plt.imshow(wc)
plt.show()

