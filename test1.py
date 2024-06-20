import streamlit as st  
import requests  
from bs4 import BeautifulSoup  
import jieba  
from wordcloud import WordCloud  
import matplotlib.pyplot as plt  
import re  
from io import BytesIO  
  
# 弹幕文本清洗函数  
def clean_danmu(text):  
    return re.sub(r'[^\u4e00-\u9fa5]', '', text)  
  
# 生成词云的函数  
def generate_wordcloud(danmu_list):  
    # 合并所有弹幕文本  
    danmustr = ' '.join(danmu_list)  
      
    # 生成词云  
    font_path = 'simsun.ttc'  # 确保此字体文件在你的环境中可用  
    wc = WordCloud(font_path=font_path, width=1000, height=1000, background_color='white')  
    wc.generate(danmustr)  
      
    # 将词云转换为图像  
    fig, ax = plt.subplots(figsize=(10, 10))  
    ax.imshow(wc, interpolation='bilinear')  
    ax.axis("off")  
    buf = BytesIO()  
    plt.savefig(buf, format="png")  
    buf.seek(0)  
      
    # 返回图像  
    return buf  
  
# Streamlit应用的主函数  
def main():  
    st.title("弹幕词云生成器")  
      
    # 假设的URL，可能需要替换  
    url = "https://comment.bilibili.com/1251331073.xml"  
      
    try:  
        response = requests.get(url)  
        response.raise_for_status()  # 检查响应状态码  
        html = response.text  
          
        # 使用lxml解析XML  
        soup = BeautifulSoup(html, 'lxml')  
          
        # 假设每个<d>标签包含弹幕文本  
        all_txt = soup.find_all("d")  # 注意：这里可能需要根据你的XML结构进行调整  
        txtss = [clean_danmu(all_txts.get_text(strip=True, separator=' ')) for all_txts in all_txt if all_txts.get_text(strip=True)]  
          
        # 生成词云图像  
        image = generate_wordcloud(txtss)  
          
        # 显示词云图像  
        st.image(image)  
          
    except requests.RequestException as e:  
        st.error(f"网络请求错误: {e}")  
    except Exception as e:  
        st.error(f"发生错误: {e}")  
  
if __name__ == "__main__":  
    main()
