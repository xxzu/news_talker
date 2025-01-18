import requests
from utils.ivs_log import LOGGER
# 定义日志配置
logger = LOGGER()
def fetch_douyin_hot_search():
    # 抖音热搜 API URL
    url = "https://www.douyin.com/aweme/v1/web/hot/search/list/?device_platform=webapp&aid=6383&channel=channel_pc_web&detail_list=1"
    
    try:
        # Step 1: 获取 Cookie
        cookie_url = "https://www.douyin.com/passport/general/login_guiding_strategy/?aid=6383"
        cookie_response = requests.get(cookie_url, headers={"User-Agent": "Mozilla/5.0"})
        
        if cookie_response.status_code != 200:
            logger.error(f"Failed to fetch cookies. Status code: {cookie_response.status_code}")
            raise Exception(f"Failed to fetch cookies. Status code: {cookie_response.status_code}")
        
        # 提取 Cookie 信息
        cookies = cookie_response.cookies.get_dict()
        cookie_string = "; ".join([f"{key}={value}" for key, value in cookies.items()])

        # Step 2: 请求热搜数据
        response = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0",
            "cookie": cookie_string
        })
        
        if response.status_code != 200:
            logger.error(f"Failed to fetch Douyin hot search data. Status code: {response.status_code}")
            raise Exception(f"Failed to fetch Douyin hot search data. Status code: {response.status_code}")

        # Step 3: 解析 JSON 数据
        if not response.text.strip():
            logger.error("douyin Received empty response from the server")
            raise Exception("Received empty response from the server")

        data = response.json()
        word_list = data.get('data', {}).get('word_list', [])
        
        # Step 4: 格式化返回数据
        hot_search_data = []
        for item in word_list:
            hot_search_data.append({
                'social_media':'抖音',
                "id": item.get("sentence_id"),
                "title": item.get("word"),
                "url": f"https://www.douyin.com/hot/{item.get('sentence_id')}"
            })

        return hot_search_data

    except Exception as e:
        logger.error(f"Error fetching Douyin hot search data: {e}")
        return []

# 示例用法
if __name__ == "__main__":
    hot_search = fetch_douyin_hot_search()
    if hot_search:
        for item in hot_search:
            print(item)
    else:
        print("No hot search data retrieved.")
