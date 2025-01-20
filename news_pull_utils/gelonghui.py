import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta,timezone
from typing import List, Dict
from utils.ivs_log import LOGGER
# 定义日志配置
logger = LOGGER()

def parse_relative_date(relative_time: str, timezone: str = "Asia/Shanghai") -> int:
    # 模拟解析相对时间的函数。需要根据实际需求调整。
    if "分钟前" in relative_time:
        minutes = int(relative_time.replace("分钟前", "").strip())
        return int((datetime.now() - timedelta(minutes=minutes)).timestamp() * 1000)
    elif "小时前" in relative_time:
        hours = int(relative_time.replace("小时前", "").strip())
        return int((datetime.now() - timedelta(hours=hours)).timestamp() * 1000)
    elif "天前" in relative_time:
        days = int(relative_time.replace("天前", "").strip())
        return int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
    else:
        # 默认返回当前时间戳
        return int(datetime.now().timestamp() * 1000)


def formatted_time(datestamp):
    from datetime import datetime

    # 时间戳（毫秒）
    

    # 转换为秒
    timestamp_s = datestamp / 1000

    # 将时间戳转换为日期对象
    date = datetime.fromtimestamp(timestamp_s,timezone.utc)

    
    local_time= date.astimezone(timezone(timedelta(hours=8)))  # UTC+8
    # 格式化为可读日期
    formatted_date = local_time.strftime("%Y-%m-%d %H:%M:%S")


    return formatted_date



def fetch_gelonghui_news() -> List[Dict]:
    try:
        base_url = "https://www.gelonghui.com"
        response = requests.get("https://www.gelonghui.com/news/")
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")
        main_content = soup.select(".article-content")

        news = []
        for el in main_content:
            a_tag = el.select_one(".detail-right > a")
            if not a_tag:
                continue

            url = a_tag.get("href")
            title = a_tag.select_one("h2").get_text(strip=True) if a_tag.select_one("h2") else ""
            info = el.select_one(".time > span:nth-child(1)").get_text(strip=True) if el.select_one(".time > span:nth-child(1)") else ""
            relative_time = el.select_one(".time > span:nth-child(3)").get_text(strip=True) if el.select_one(".time > span:nth-child(3)") else ""

            if url and title and relative_time:
                news.append({
                    'social_media':'格隆汇',
                    "url": base_url + url,
                    "title": title,
                    "id": url,
                    
                    "date": formatted_time(parse_relative_date(relative_time)),
                    "info": info,
                    
                })

        return news
    except Exception as e:
        logger.error(f'格隆汇数据抓取失败：{e}')
        return []

if __name__ == "__main__":
    news_items = fetch_gelonghui_news()
    for item in news_items:
        print(item)
