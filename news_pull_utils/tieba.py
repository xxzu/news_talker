import requests
from utils.ivs_log import LOGGER
# 定义日志配置
logger = LOGGER()

def get_baidu_tieba_hot_topics():
    # API URL
    url = "https://tieba.baidu.com/hottopic/browse/topicList"
    
    # 发送 GET 请求获取数据
    try:
        response = requests.get(url)
        response.raise_for_status()  # 确保请求成功
        
        # 解析 JSON 响应数据
        data = response.json().get('data', {}).get('bang_topic', {}).get('topic_list', [])
        
        # 提取并返回数据
        hot_topics = [
            {
                'social_media':'贴吧',
                'id': item['topic_id'],
                'title': item['topic_name'],
                'url': item['topic_url']
            }
            for item in data
        ]
        
        return hot_topics
    except Exception as e:
        logger(f"获取数据时发生错误: {e}")
        return []

# 获取并打印热门话题数据
if __name__ == '__main__':
    hot_topics = get_baidu_tieba_hot_topics()
    for topic in hot_topics:
        print(topic)
