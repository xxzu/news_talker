import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import pytz
from utils.ivs_log import LOGGER
# 定义日志配置
logger = LOGGER()
from datetime import datetime







def parse_relative_date(relative_date, timezone="Asia/Shanghai"):
    """
    Convert a relative date (e.g., '2小时前', '1天前') to a timestamp.
    """
    now = datetime.now(pytz.timezone(timezone))
    if "小时前" in relative_date:
        hours = int(relative_date.replace("小时前", "").strip())
        return (now - timedelta(hours=hours)).timestamp()
    elif "分钟前" in relative_date:
        minutes = int(relative_date.replace("分钟前", "").strip())
        return (now - timedelta(minutes=minutes)).timestamp()
    elif "天前" in relative_date:
        days = int(relative_date.replace("天前", "").strip())
        return (now - timedelta(days=days)).timestamp()
    else:
        # If the date is not relative, return the current time
        return now.timestamp()

def get_36kr_newsflashes():
    """
    Scrape the 36氪快讯页面 and return a list of news items.
    """
    base_url = "https://www.36kr.com"
    url = f"{base_url}/newsflashes"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
    }

    try:
        # Fetch the webpage
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        html_content = response.text

        # Parse the HTML content
        soup = BeautifulSoup(html_content, "html.parser")
        news_items = []

        # Extract newsflash items
        items = soup.select(".newsflash-item")
        for item in items:
            title_element = item.select_one("a.item-title")
            time_element = item.select_one(".time")

            if title_element and time_element:
                news_url = title_element["href"]
                title = title_element.get_text(strip=True)
                relative_date = time_element.get_text(strip=True)
                timestamp = parse_relative_date(relative_date, "Asia/Shanghai")
                # 转换为日期时间格式
                readable_date = datetime.fromtimestamp(timestamp)

                # 以指定格式输出日期时间
                formatted_date = readable_date.strftime("%Y-%m-%d %H:%M:%S")
                
                news_items.append({
                    "social_media":"36kr",
                    "url": f"{base_url}{news_url}",
                    "title": title,
                    "id": news_url,
                    
                    "date": formatted_date
                    
                })

        return news_items

    except requests.RequestException as e:
        logger.error(f"Error fetching 36kr newsflashes: {e}")
        return []

# Example usage
if __name__ == "__main__":
    news = get_36kr_newsflashes()
    for item in news:
        print(item)
