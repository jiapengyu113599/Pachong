import streamlit as st
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import requests
import re
import jieba

def main():
    st.title('Bilibili DanMu Word Cloud')

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
    words = ' '.join(jieba.lcut(DanMu_text))

    # 设置词云图的宽度和高度
    word_cloud_width = 800  # 宽度，单位为像素
    word_cloud_height = 600  # 高度，单位为像素

    # 生成词云图
    wordcloud = WordCloud(font_path='./SIMHEI.TTF',  # 确保路径正确
                           width=word_cloud_width,
                           height=word_cloud_height,
                           background_color='white', 
                           max_words=100, 
                           max_font_size=100).generate(words)

    # 显示词云图
    # 使用原始大小的DPI以避免图像模糊
    plt.figure(dpi=72, figsize=(word_cloud_width / 72, word_cloud_height / 72))
    plt.imshow(wordcloud, interpolation='bicubic')  # 使用 bicubic 插值以提高图像质量
    plt.axis("off")
    plt.tight_layout(pad=0)

    # 显示图表
    st.pyplot(plt)

if __name__ == "__main__":
    main()
