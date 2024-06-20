import streamlit as st
import requests
import re
import jieba
from collections import Counter
import matplotlib.pyplot as plt

# 导入字体设置
from matplotlib.font_manager import FontProperties

def main():
    st.title('Bilibili DanMu Word Frequency')

    # 用户输入oid
    oid = st.text_input("请输入Bilibili视频的oid:")

    # 检查用户是否输入了oid
    if not oid:
        st.error("没有输入oid，请重新输入！")
        return

    # 爬取网页源码
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    response = requests.get(f"https://api.bilibili.com/x/v1/dm/list.so?oid={oid}", headers=headers)
    
    # 如果请求失败，显示错误信息
    if response.status_code != 200:
        st.error(f"请求失败，状态码：{response.status_code}")
        return
    
    html_doc = response.content.decode('utf-8')

    # 弹幕匹配
    format = re.compile(r'<d.*?>(.*?)</d>')
    DanMu_list = format.findall(html_doc)

    # 合并弹幕
    DanMu_text = ' '.join(DanMu_list)

    # 分词
    words = jieba.lcut(DanMu_text)

    # 统计词频
    word_counts = Counter(words)

    # 获取最常见的词和它们的频率
    most_common_words = word_counts.most_common(10)  # 这里取最常见的10个词

    # 设置matplotlib字体为中文
    plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
    plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号

    # 绘制条形图
    words, counts = zip(*most_common_words)  # 解包最常见的词和它们的频率
    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color='skyblue')
    plt.xlabel('Frequency', fontsize=12)  # 指定字体大小
    plt.ylabel('Words', fontsize=12)
    plt.title('Top 10 Most Common Words in DanMu', fontsize=14)

    # 将图表转换为图片并展示在Streamlit中
    plt_image = plt.gcf()  # 获取当前图表对象
    st.pyplot(plt_image)

if __name__ == "__main__":
    main()
