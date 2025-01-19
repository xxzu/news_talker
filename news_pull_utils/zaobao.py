import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz

def parse_relative_date(relative_date, timezone="Asia/Shanghai"):
    # 自定义解析相对时间的逻辑（需要根据实际格式调整）
    tz = pytz.timezone(timezone)
    now = datetime.now(tz)
    if "分钟前" in relative_date:
        minutes = int(relative_date.replace("分钟前", "").strip())
        return now - timedelta(minutes=minutes)
    elif "小时前" in relative_date:
        hours = int(relative_date.replace("小时前", "").strip())
        return now - timedelta(hours=hours)
    elif "昨天" in relative_date:
        return (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    # 默认返回当前时间
    return now

def fetch_description(url):
    try:
        base = "https://www.kzaobao.com"
        response = requests.get(base + url)
        response.encoding = "gb2312"
        soup = BeautifulSoup(response.text, "html.parser")
        content = "\n".join([p.text.strip() for p in soup.select(".viewbox .content p")])
        return content
    except Exception as e:
        return ""
    




def fetch_zaobao_news():
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
            
            if url and title and date_text:
                description = fetch_description(url)
                news_items.append({
                    "social_media":'zaobao',
                    "url": base + url,
                    "title": title,
                    "id": url,
                    "date": date_text,
                    "description":description
                })

    # 按发布时间排序
    # sorted_times = sorted(time_strings, key=lambda x: datetime.strptime(x, '%Y-%m-%d %H:%M:%S'))
    news_items.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d %H:%M:%S'), reverse=True)
    return news_items

if __name__ == "__main__":
    news = fetch_zaobao_news()
    for item in news:
        print(item)
