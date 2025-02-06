from utils.ivs_log import LOGGER
logger = LOGGER()
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from utils.ivs_log import LOGGER

# 定义日志配置
logger = LOGGER()

def fetch_description(url):
    try:
        base = "https://www.kzaobao.com"
        response = requests.get(base + url)
        response.encoding = "gb2312"
        # soup = BeautifulSoup(response.text, "html.parser")
        soup = BeautifulSoup(response.text, "lxml")

        content = "\n".join([p.text.strip() for p in soup.select(".viewbox .content p")])
        return content
    except Exception as e:
        logger.error( f"抓取早报内容错误：{e}")
        return ' '
    

def fetch_zaobao_news():
    try:
        url = "https://www.kzaobao.com/top.html"
        base = "https://www.kzaobao.com"
        
        # 获取 GB2312 编码的页面
        response = requests.get(url)
        response.encoding = "gb2312"
        
        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, "html.parser")
        news_items = []

        # 查找特定的 div 和 tr 元素
        main_content = soup.select("div[id^='cd0'] tr")
        for element in main_content:
            a_tag = element.select_one("h3 > a")
            
            if a_tag:
                url = a_tag.get("href")
                title = a_tag.text.strip()
                date_text = element.select_one("td:nth-child(3)").text.strip()

                # 解析时间为 datetime 对象
                try:
                    date = datetime.strptime(date_text, '%Y-%m-%d %H:%M:%S')
                except ValueError as e:
                    logger.error(f"日期格式错误: {e}")
                    continue

                if url and title and date_text:
                    description = fetch_description(url)
                    news_items.append({
                        "social_media": '联合早报',
                        "url": base + url,
                        "title": title,
                        "id": url,
                        "date": date.isoformat().replace("T", " "),  # 转换为 ISO 格式的字符串
                        "description": description
                    })

        # 按发布时间排序，使用 datetime 对象进行排序
        news_items.sort(key=lambda x: x['date'], reverse=True)
        return news_items
    except Exception as e:
        logger.error(f"抓取早报新闻错误：{e}")
        return []


if __name__ == "__main__":
    news = fetch_zaobao_news()
    for item in news:
        print(f"Title: {item['title']}")
        print(f"URL: {item['url']}")
        print(f"Date: {item['date']}")  # 这里打印的是 ISO 格式的字符串
        print(f"Description: {item['description']}\n")
