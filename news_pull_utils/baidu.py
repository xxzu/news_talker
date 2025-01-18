import requests
import re
import json
import sys
sys.path.append('.')
from utils.ivs_log import LOGGER
# 定义日志配置
logger = LOGGER()

def get_baidu_hot_search():
    
    url = "https://top.baidu.com/board?tab=realtime"
    try:
        # 获取百度热搜页面的原始 HTML 数据
        response = requests.get(url)
        
        if response.status_code != 200:
            raise Exception("无法获取百度热搜页面数据")
        
        raw_data = response.text
        
        # 使用正则表达式提取出 JSON 数据
        match = re.search(r"<!--s-data:(.*?)-->", raw_data, re.S)
        
        if not match:
            
            raise Exception("无法提取百度热搜数据")
        
        # 解析 JSON 数据
        data = json.loads(match.group(1))
        
        # 提取并格式化热搜数据
        hot_search_data = []
        for item in data.get('data', {}).get('cards', [])[0].get('content', []):
            if not item.get('isTop'):  # 过滤掉置顶的热搜
                hot_item_data = {
                    'social_media':"百度",
                    'id': item['rawUrl'],
                    'title': item['word'],
                    'url': item['rawUrl'],
                    
                }
                hot_search_data.append(hot_item_data)
        
        return hot_search_data
    except Exception as e:
        logger(f"获取热搜数据时发生错误: {e}")
        return []

# 示例用法
if __name__ == '__main__':
    try:
        hot_search = get_baidu_hot_search()
        for item in hot_search:
            print(item)
    except Exception as e:
        logger(f"获取热搜数据时发生错误: {e}")
