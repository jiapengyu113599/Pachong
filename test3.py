import streamlit as st
import requests
import re
import jieba
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties

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

    # 绘制条形图之前，设置字体
    font_path = "./SIMHEI.TTF"  # 确保这里是字体文件的相对路径或绝对路径
    chinese_font = FontProperties(fname=font_path)

    words, counts = zip(*most_common_words)  # 解包最常见的词和它们的频率
    plt.figure(figsize=(10, 6))
    plt.barh(words, counts, color='skyblue')

    # 直接使用FontProperties设置中文
    plt.xlabel('频率', fontproperties=chinese_font)
    plt.ylabel('词语', fontproperties=chinese_font)
    plt.title('弹幕词频统计', fontproperties=chinese_font)

    # 保存图表为临时图片文件
    plt.savefig('temp_plot.png')

    # 展示图表
    st.image('temp_plot.png', use_column_width=True)

if __name__ == "__main__":
    main()

