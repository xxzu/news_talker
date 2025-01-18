import requests

from urllib.parse import quote
from utils.ivs_log import LOGGER
# 定义日志配置
logger = LOGGER()

def get_bilibili_hot_search():
    
    url = "https://s.search.bilibili.com/main/hotword?limit=30"
    try: 
    # 获取 Bilibili 热搜数据
        response = requests.get(url)
        
        response.raise_for_status()
        
        data = response.json()
        
        # 提取热搜数据并转换为所需格式
        hot_search_data = []
        for item in data.get('list', []):
            hot_item_data = {
                'social_media':'bilibili',
                'id': item['keyword'],
                'title': item['show_name'],
                'url': f"https://search.bilibili.com/all?keyword={quote(item['keyword'])}",
                
            }
            hot_search_data.append(hot_item_data)
    
        return hot_search_data
    except Exception as e:
        logger(f"获取热搜数据时发生错误: {e}")
        return []

# 示例用法
if __name__ == '__main__':
    try:
        hot_search = get_bilibili_hot_search()
        for item in hot_search:
            print(item)
    except Exception as e:
        print(f"获取热搜数据时发生错误: {e}")
