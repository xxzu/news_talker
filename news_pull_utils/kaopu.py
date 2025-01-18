import requests
from utils.ivs_log import LOGGER
# 定义日志配置
logger = LOGGER()
def fetch_kaopu_news_data():
    urls = [
        "https://kaopucdn.azureedge.net/jsondata/news_list_beta_hans_0.json",
        "https://kaopucdn.azureedge.net/jsondata/news_list_beta_hans_1.json"
    ]
    
    all_news = []
    
    for url in urls:
        try:
            # Fetch the JSON data
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            # Filter out specific publishers
            filtered_data = [
                {
                    'social_media':'kaopu',
                    "id": item["link"],
                    "title": item["title"],
                    "date": item["pubDate"][:10],
                    "channelName": item["publisher"],
                    "extra": {
                        "hover": item["description"],
                        
                    },
                    "url": item["link"]
                }
                for item in data if item["publisher"] not in ["财新", "公视"]
            ]
            
            all_news.extend(filtered_data)
        
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching data from {url}: {e}")
    
    return all_news


if __name__ == '__main__':
    news_data = fetch_kaopu_news_data()
    for news in news_data:
        print(news)
