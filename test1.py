import streamlit as st  
import requests  
from bs4 import BeautifulSoup  
import jieba  
from wordcloud import WordCloud  
import matplotlib.pyplot as plt  
from PIL import Image  
import numpy as np  
  
# 假设你已经在本地或云端提供了'simsun.ttc'字体文件  
FONT_PATH = 'simsun.ttc'  # 确保这个字体文件在你的应用目录中  
  
def generate_wordcloud(txtsss):  
    danmustr = ''.join(txtsss)  
    words = list(jieba.cut(danmustr))  
    words = [i for i in words if len(i) > 1]  
    wc = WordCloud(height=1000, width=1000, font_path=FONT_PATH, background_color='white')  
    wc.generate(' '.join(words))  
    return wc  
  
def plot_wordcloud(wc):  
    plt.figure(figsize=(10, 10), facecolor=None)  
    plt.imshow(wc, interpolation="bilinear")  
    plt.axis("off")  
    plt.tight_layout(pad=0)  
      
    # 将matplotlib图像转换为PIL图像，以便在Streamlit中显示  
    buf = io.BytesIO()  
    plt.savefig(buf, format='png')  
    buf.seek(0)  
    image = Image.open(buf)  
    image = image.convert('RGB')  
    return image  
  
def main():  
    url = "https://comment.bilibili.com/1251331073.xml"  
    response = requests.get(url)  
    response.encoding = 'utf-8'  
    html = response.text  
    soup = BeautifulSoup(html, "xml")  
    all_txt = soup.findAll("d")  
    txtss = [all_txts.string for all_txts in all_txt if all_txts.string]  # 确保只取有内容的字符串  
    txtsss = [txts.replace(' ', '') for txts in txtss]  
  
    wc = generate_wordcloud(txtsss)  
    image = plot_wordcloud(wc)  
  
    # 在Streamlit中显示词云  
    st.image(image, caption='Bilibili Comment Word Cloud')  
  
if __name__ == "__main__":  
    main()
