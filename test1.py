import streamlit as st
from bs4 import BeautifulSoup
import requests
import re
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

def main():
    st.title('Bilibili DanMu Word Cloud')

    # 爬取网页源码
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    response = requests.get("https://api.bilibili.com/x/v1/dm/list.so?oid=130684654", headers=headers)
    html_doc = response.content.decode('utf-8')

    # 弹幕匹配
    format = re.compile(r'<d.*?>(.*?)</d>')
    DanMu_list = format.findall(html_doc)

    # 合并弹幕
    DanMu_text = ' '.join(DanMu_list)

    # 分词
    words = jieba.lcut(DanMu_text)

    # 生成词云图
    wordcloud = WordCloud(font_path='SIMHEI.TTF', background_color='white', max_words=100, max_font_size=100).generate(' '.join(words))

    # 显示词云图
    fig = plt.figure(figsize=(10, 8), facecolor=None)
    plt.imshow(wordcloud)
    plt.axis("off")
    plt.tight_layout(pad=0)
    st.pyplot(fig)

if __name__ == "__main__":
    main()
