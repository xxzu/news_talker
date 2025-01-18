
import requests

from urllib.parse import urlencode,quote
from utils.ivs_log import LOGGER

# 定义日志配置
logger = LOGGER()
import hashlib







def fetch_weibo_hot_search():
    try:
        url = "https://weibo.com/ajax/side/hotSearch"
        
        # 发送请求并解析响应
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功
        res = response.json()  # 将返回的 JSON 数据解析为字典
        
        # 数据处理逻辑
        results = []
        for item in res.get('data', {}).get('realtime', []):
            if item.get('is_ad'):  # 过滤广告
                continue
            
            # 构建关键词
            keyword = item.get('word_scheme') or f"#{item['word']}#"
            hash_value = hashlib.sha256(keyword.encode('utf-8')).hexdigest()
            # 构建结果项
            result = {
                "social_media":"微博",
                "id": hash_value,# num 会变化，估计这里是热度值
                "title": item['word'],
                "rank":item.get('rank',float('inf')) + 1,
                "url": f"https://s.weibo.com/weibo?q={quote(keyword)}"
                
            }
            results.append(result)
        results = sorted(results,key=lambda x : x['rank'])[:10]
        return results
    except Exception as e:
        logger.error(f'抓取微博消息出现问题{e}')
        return []

# 调用函数获取热搜数据
if __name__ == "__main__":
    hot_searches = fetch_weibo_hot_search()
    for search in hot_searches:
        print(search)
