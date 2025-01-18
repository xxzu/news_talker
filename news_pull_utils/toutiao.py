import requests
from utils.ivs_log import LOGGER
# 定义日志配置
logger = LOGGER()

def get_toutiao_hot():
    # API URL
    try:
        url = "https://www.toutiao.com/hot-event/hot-board/?origin=toutiao_pc"
        
        # 发送 GET 请求获取数据
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功，若失败会抛出异常
        
        # 解析 JSON 响应数据
        data = response.json().get('data', [])
        
        # 提取并返回数据
        trending_data = [
            {
                'social_media': '头条',
                'id': item['ClusterIdStr'],
                'title': item['Title'],
                'url': f"https://www.toutiao.com/trending/{item['ClusterIdStr']}/"
            }
            for item in data
        ]
        
        return trending_data
       
    except Exception as e:
        # 打印详细的错误信息
        logger(f'头条信息抓取错误！错误信息: {e}')
        return []

# 获取并打印热搜数据
if __name__ == '__main__':
    hot_trending = get_toutiao_hot()
    if hot_trending:
        for item in hot_trending:
            print(item)
