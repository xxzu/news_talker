import requests
from datetime import datetime
from typing import List, Dict
from utils.ivs_log import LOGGER
# 定义日志配置
logger = LOGGER()

import time

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
}


def fetch_cankaoxinxi_news() -> List[Dict]:
    # 定义需要请求的频道
    channels = ["zhongguo", "guandian", "gj"]
    base_url = "https://china.cankaoxiaoxi.com/json/channel"
    retries = 3
    for _ in range(retries):
        try:
            all_data = []
            for channel in channels:
                # 构造 URL 并请求数据
                url = f"{base_url}/{channel}/list.json"
                response = requests.get(url, headers=headers, timeout=10)
                if response.status_code == 200:
                    res_data = response.json()
                    if "list" in res_data:
                        all_data.extend(res_data["list"])
                else:
                    logger.error(f"Failed to fetch data from {url}, status code: {response.status_code}")

            # 转换和排序数据
            result = []
            for item in all_data:
                data = item.get("data", {})
                
                result.append({
                    'social_media':"参考消息",
                    "date":data.get("createtime",""),
                    "channelName":data.get("channelName",""),
                    "id": data.get("id"),
                    "title": data.get("title"),
                    "url": data.get("url"),
                    
                    # "date": publish_time
                    
                })

            # 按时间排序
            sorted_result = sorted(result, key=lambda x: x["date"], reverse=True)
            return sorted_result
        except requests.RequestException as e:
            logger.error(f"请求失败: {e}")
            time.sleep(2)  # Wait before retrying
        else:
            break  # If successful, exit the loop

    return []  



# 示例用法
if __name__ == "__main__":
    news_data = fetch_cankaoxinxi_news()
    for news in news_data:
        print(news)
