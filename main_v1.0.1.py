import os
import sys
import time
import schedule
import json
from itertools import chain

from utils.ivs_log import LOGGER
# 定义日志配置
logger = LOGGER()
from news_pull_utils.zhihu import get_zhihu_hot
from news_pull_utils.weibo import fetch_weibo_hot_search
from news_pull_utils.toutiao import get_toutiao_hot
from news_pull_utils.tieba import get_baidu_tieba_hot_topics
from news_pull_utils.bilibili import get_bilibili_hot_search


from telegram_utils.sand_to_tg import send_to_telegram
from redis_server.redis_utils import RedisHandler
from dotenv import load_dotenv

load_dotenv()
REDIS_SERVER = os.getenv('REDIS_SERVER')
REDIS_PUSHED = os.getenv('REDIS_PUSHED')
INTERVAL_TIME_NEWS = os.getenv('INTERVAL_TIME_NEWS')
INTERVAL_TIME = os.getenv('INTERVAL_TIME')

# 初始化 Redis 连接
redis_server = RedisHandler(set_key=REDIS_SERVER)
redis_pushed = RedisHandler(set_key=REDIS_PUSHED)




# 获取并存储热搜数据到 Redis
def save_messages_to_redis():
    try:
        bilibili_hot_list = get_bilibili_hot_search()
        tieba_hot_list = get_baidu_tieba_hot_topics()
        zhihu_hot_list = get_zhihu_hot()
        weibo_hot_list = fetch_weibo_hot_search()
        toutiao_hot_list = get_toutiao_hot()
        combined_news_hot_list = list(chain(zhihu_hot_list, weibo_hot_list, toutiao_hot_list,tieba_hot_list,bilibili_hot_list))
        
        for item in combined_news_hot_list:
            # logging.info(f"获取到数据：{item}")
            json_item = json.dumps(item)
            item_id = item.get('id')

            if redis_pushed.is_in_set(str(item_id)):
                continue  # 跳过已推送的消息

            redis_server.add_to_set(json_item)
    except Exception as e:
        logger.error(f"保存消息到 Redis 时发生错误: {e}")

# 推送数据到 Telegram
def push_news_hot_to_telegram():
    

    try:
        if redis_server.get_set_length() != 0:
            item = redis_server.random_pop_messages()
            
            json_item = json.loads(item)

            if not redis_pushed.is_in_set(str(json_item['id'])):
                message = format_message(json_item)
                send_to_telegram(message)

                redis_pushed.add_to_set(str(json_item['id']))

            time.sleep(3)  # 每条消息之间等待 3 秒
    except Exception as e:
        logger.error(f"推送消息时发生错误: {e}")

# 格式化消息
def format_message(json_item):
    if json_item['social_media'] == '微博':
        return f"<b><i>[{json_item['social_media']}]</i></b>：<a href=\"{json_item['url']}\">{json_item['title']}</a>\n热搜排行：<b>{json_item['rank']}</b>"
    else:
        return f"<b><i>[{json_item['social_media']}]</i></b>：<a href=\"{json_item['url']}\">{json_item['title']}</a>"

# 主程序运行
if __name__ == "__main__":
    schedule.every(INTERVAL_TIME_NEWS).seconds.do(save_messages_to_redis)
    schedule.every(INTERVAL_TIME).seconds.do(push_news_hot_to_telegram)

    logger.info('程序启动成功！')

    while True:
        schedule.run_pending()
        time.sleep(1)
