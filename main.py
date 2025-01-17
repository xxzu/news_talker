import os
import sys
import time
import schedule
import json

sys.path.append('.')


from news_pull_utils.zhihu import get_zhihu_hot
from telegram_utils.sand_to_tg import send_to_telegram
from redis_server.redis_utils import RedisHandler


from dotenv import load_dotenv
load_dotenv()
REDIS_SERVER_ZHIHU = os.getenv('REDIS_SERVER_ZHIHU')
REDIS_ZHIHU_PUSHED = os.getenv('REDIS_ZHIHU_PUSHED')


# 初始化 Redis 连接
redis_server_zhihu = RedisHandler(set_key=REDIS_SERVER_ZHIHU )
redis_zhihu_pushed = RedisHandler(set_key=REDIS_ZHIHU_PUSHED)

# 定义延时函数
def delay(seconds):
    time.sleep(seconds)

# 定义获取热点的时间间隔（以秒为单位，例如 10 秒）
INTERVAL_TIME = 5

# 存储新的知乎数据到 Redis
def save_messages_to_redis():
    zhihu_hot_list = get_zhihu_hot()
    
    for item in zhihu_hot_list:
        
        
        json_item = json.dumps(item)
        item_id = item.get('id') 
        # item_id = item['id'] # 获取唯一 id
       
        
        # 判断该 id 是否已经推送过
        if redis_zhihu_pushed.is_in_set(str(item_id)):
            continue  # 如果已推送过该数据，则跳过

        # 将新数据存入 Redis 集合
        redis_server_zhihu.add_to_set(json_item)
        

def push_zhihu_hot_to_telegram():
    print("程序开始执行...")

    try:
        if redis_server_zhihu.get_set_length() != 0:
            item = redis_server_zhihu.random_pop_messages()
            # print('获取到的消息:', item)
            
            # 将 item 从字符串解析为字典
            json_item = json.loads(item)
            
            # 检查该 id 是否已经推送过
            if not redis_zhihu_pushed.is_in_set(str(json_item['id'])):
                message = f"<b>{json_item['title']}</b>\n<a href=\"{json_item['url']}\">查看详情</a>"
                send_to_telegram(message)
                # 将已推送的 id 存入 Redis
                redis_zhihu_pushed.add_to_set(str(json_item['id']))
            
            delay(3)  # 每条消息之间等待 3 秒
    except Exception as e:
        print('获取热点或发送消息时发生错误:', e)

# 主程序运行
if __name__ == "__main__":
    # # # 不清空 Redis 数据，避免每次启动都丢失数据
    # redis_server_zhihu.clear_database()
    # redis_zhihu_pushed.clear_database()

    # print("每次启动判断数据展示", redis_server_zhihu.get_all_from_set())  # []

    # 定时任务：每隔 INTERVAL_TIME 秒运行一次
    schedule.every(INTERVAL_TIME).seconds.do(save_messages_to_redis)
    schedule.every(INTERVAL_TIME).seconds.do(push_zhihu_hot_to_telegram)

    # 启动定时任务
    
    while True:
        schedule.run_pending()
        time.sleep(1)
    #    save_messages_to_redis()
    #    push_zhihu_hot_to_telegram()
