import random
import requests
import re
import jieba
from wordcloud import WordCloud
import matplotlib.pyplot as plt


def get_video_id_from_url(url):
    # 解析视频ID的逻辑，这取决于Bilibili的URL结构
    # 这里只是一个示例，实际逻辑可能不同
    video_id = re.search(r'BV(\w+)', url).group(1)  # 假设Bilibili的新链接格式是BVxxxxxx
    return video_id


def get_danmu_from_api(video_id, headers):
    # 模拟从API获取弹幕数据的过程
    danmu_data = [
        "弹幕1", "弹幕2", "这是弹幕3", "中文字符弹幕", "又一个弹幕示例"
    ]
    return danmu_data

def generate_wordcloud(danmu_text):
    # 检查danmu_text是否为空
    if not danmu_text or not danmu_text.strip():
        print("没有有效的弹幕数据来生成词云。")
        return

    words = jieba.lcut(danmu_text)

    # 随机化单词顺序（可选）
    random.shuffle(words)


    wordcloud = WordCloud(font_path='simhei.ttf',  # 设置字体文件路径，确保能够显示中文
                      background_color='white',  # 设置背景颜色
                      max_words=100,  # 最多显示的词数
                      max_font_size=100  # 字体最大值
                      ).generate(' '.join(words))

# 显示词云图
    plt.figure(figsize=(10, 8), facecolor=None)  # 创建一个绘图对象
    plt.imshow(wordcloud)  # 显示词云图
    plt.axis("off")  # 不显示坐标轴
    plt.tight_layout(pad=0)  # 调整子图参数，使之填充整个图像区域
    plt.show()  # 显示图像


def main():
    video_url = input("请输入Bilibili视频网址：")
    video_id = get_video_id_from_url(video_url)
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36",
    }
    danmu_data = get_danmu_from_api(video_id, headers)
    if not danmu_data:
        print("从API获取弹幕数据时出错或没有获取到任何数据。")
        return
    print("获取到的弹幕数据（部分）：")
    print(danmu_data[:10])  # 打印前10条弹幕，以便检查数据是否变化
    danmu_text = ' '.join(danmu_data)  # 合并所有弹幕到一个字符串中
    generate_wordcloud(danmu_text)  # 生成词云图

if __name__ == "__main__":
    main()
