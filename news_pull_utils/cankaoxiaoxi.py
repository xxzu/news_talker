import requests
from datetime import datetime
from typing import List, Dict
from utils.ivs_log import LOGGER
# 定义日志配置
logger = LOGGER()
def fetch_cankaoxinxi_news() -> List[Dict]:
    # 定义需要请求的频道
    channels = ["zhongguo", "guandian", "gj"]
    base_url = "https://china.cankaoxiaoxi.com/json/channel"

    all_data = []
    for channel in channels:
        # 构造 URL 并请求数据
        url = f"{base_url}/{channel}/list.json"
        response = requests.get(url)
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
        # publish_time =data.get("publishTime", "")
        # # 转换为日期时间格式
        
        # readable_date = datetime.fromtimestamp(timestamp)

        # # 以指定格式输出日期时间
        # formatted_date = readable_date.strftime("%Y-%m-%d %H:%M:%S")
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



# 示例用法
if __name__ == "__main__":
    news_data = fetch_cankaoxinxi_news()
    for news in news_data:
        print(news)
