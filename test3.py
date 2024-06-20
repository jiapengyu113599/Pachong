import streamlit as st
import requests
import re
import jieba
from collections import Counter
import matplotlib.pyplot as plt
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
    
    html_doc = response.content.decode('utf-8', errors='ignore')

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
    most_common_words = word_counts.most_common(10)

    # 注册字体
    font_path = 'SIMHEI.TTF'  # 确保这个路径是正确的
    font_prop = FontProperties(fname=font_path)

    # 绘制条形图
    plt.figure(figsize=(10, 6))
    bars = plt.barh(range(len(most_common_words)), [count for _, count in most_common_words], color='skyblue')
    for i, (word, count) in enumerate(most_common_words):
        plt.text(counts[i], i, f'{word}\n{count}', va='center', fontproperties=font_prop, color='black')

    plt.xlabel('Frequency', fontproperties=font_prop)
    plt.ylabel('Words', fontproperties=font_prop)
    plt.title('Top 10 Most Common Words in DanMu', fontproperties=font_prop)

    # 显示图表
    plt.tight_layout()  # 确保布局适合显示中文
    st.pyplot(plt)

if __name__ == "__main__":
    main()
