import requests
import time
from bs4 import BeautifulSoup
from typing import List, Dict
from datetime import datetime, timedelta, timezone
from utils.ivs_log import LOGGER
import re

logger = LOGGER()



headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
}

def get_time():
    timestamp_s = time.time()
    date = datetime.fromtimestamp(timestamp_s, timezone.utc)
    local_time = date.astimezone(timezone(timedelta(hours=8)))  # UTC+8
    formatted_date = local_time.strftime("%Y-%m-%d ")
    return formatted_date

def fetch_jinse_news() -> List[Dict]:
    retries = 3
    for _ in range(retries):
        try:
            base_url = "https://www.jinse.cn"
            response = requests.get(f"{base_url}/lives/", headers=headers, timeout=10)
            response.raise_for_status()  # Check if the request was successful
            soup = BeautifulSoup(response.text, "html.parser")
            main_content = soup.select("div.js-lives__item")
            news_list = []

            for element in main_content:
                a_tag = element.select_one("a.title")
                title = a_tag.text.strip() if a_tag else "无标题"
                link = base_url + a_tag["href"] if a_tag and "href" in a_tag.attrs else "无链接"
                time_tag = element.select_one(".time")
                
                if time_tag:
                    news_time = get_time() + " " + time_tag.text.strip()
                else:
                    news_time = "无时间"
                
                description = element.select_one('div.content > a:nth-of-type(2)').text.strip()
                
                description = re.sub(r"【" + re.escape(title) + "】", "", description)
                description = re.sub(r'金色财经报道,',"",description)
                # positive = element.select_one('a.like.rose-h').text.strip() if element.select_one('a.like.rose-h') else "无利好"
                # negative = element.select_one('a.like.fall').text.strip() if element.select_one('a.like.fall') else "无利空"

                news_list.append({
                    'social_media': "金色财经",
                    "date": news_time,
                    "title": title,
                    "description": description,
                    "url": link,
                    # "emotions": f"[{positive}] [{negative}]",
                    'id': link
                })
            return news_list

        except requests.RequestException as e:
            logger.error(f"请求失败: {e}")
            time.sleep(2)  # Wait before retrying
            continue
        else:
            break  # If successful, exit the loop

    return []  # Return an empty list if all retries fail

# Example usage:
if __name__ == "__main__":
    news = fetch_jinse_news()
    print(news)
    