import os
import sys
import time
import schedule
import json
from itertools import chain

from utils.ivs_log import LOGGER
# 定义日志配置
logger = LOGGER()
from news_pull_utils import *

from telegram_utils.sand_to_tg import send_to_telegram
from redis_server.redis_utils import RedisHandler
from dotenv import load_dotenv

load_dotenv()
REDIS_SERVER = os.getenv('REDIS_SERVER')
REDIS_PUSHED = os.getenv('REDIS_PUSHED')
INTERVAL_TIME_NEWS = int(os.getenv('INTERVAL_TIME_NEWS'))
INTERVAL_TIME = int(os.getenv('INTERVAL_TIME'))

# 初始化 Redis 连接
redis_server = RedisHandler(set_key=REDIS_SERVER)
redis_pushed = RedisHandler(set_key=REDIS_PUSHED)




# 获取并存储热搜数据到 Redis
def save_messages_to_redis():
    try:
        baidu_news_list = get_baidu_hot_search()
        bilibili_hot_list = get_bilibili_hot_search()
        tieba_hot_list = get_baidu_tieba_hot_topics()
        zhihu_hot_list = get_zhihu_hot()
        weibo_hot_list = fetch_weibo_hot_search()
        toutiao_hot_list = get_toutiao_hot()
        douyin_hot_list = fetch_douyin_hot_search()
        news36kr_hot_list = get_36kr_newsflashes()
        combined_news_hot_list = list(
                        chain(
                            zhihu_hot_list,
                            weibo_hot_list, 
                            toutiao_hot_list,
                            tieba_hot_list,
                            bilibili_hot_list,
                            baidu_news_list,
                            douyin_hot_list,
                            news36kr_hot_list,
                            fetch_cankaoxinxi_news(),
                            fetch_kaopu_news_data(),
                            
                            
                            
                            ))
        
        
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
            #logger.info(f'消息推送：{json_item}')

            if not redis_pushed.is_in_set(str(json_item['id'])):
                message = format_message(json_item)
                send_to_telegram(message)

                redis_pushed.add_to_set(str(json_item['id']))

            time.sleep(3)  # 每条消息之间等待 3 秒
    except Exception as e:
        logger.error(f"推送消息时发生错误: {e}")

# 格式化消息
def format_message(json_item):
    try:
        if json_item['social_media'] == '微博':
            return f"<b>[{json_item['social_media']}]</b>：<a href=\"{json_item['url']}\">{json_item['title']}</a>\n热搜实时排行：<b>{json_item['rank']}</b>"
        elif json_item['social_media'] == '36kr':
            return f"<b>[{json_item['social_media']}]</b>：<a href=\"{json_item['url']}\">{json_item['title']}</a>\n新闻时间：<b>{json_item['date']}</b>"
        elif json_item['social_media'] =="参考消息":
            # logger.info(f"<b>[{json_item['social_media']}:{json_item['channelName']}]</b>：<a href=\"{json_item['url']}\">{json_item['title']}</a>\n新闻时间：<b>{json_item['date']}</b>")
            return f"<b>[{json_item['social_media']}:{json_item['channelName']}]</b>：<a href=\"{json_item['url']}\">{json_item['title']}</a>\n新闻时间：<b>{json_item['date']}</b>"
        elif json_item['social_media'] == 'kaopu':
            # title = json_item['title']
            hover_description = json_item['extra']['hover'][:150]
            url = json_item['url']
            
            # Full description in the message
            message = f"<b>[{json_item['social_media']}:{json_item['channelName']}]</b>:"
            # message += f"<b>{title}</b>\n"  # Title as bold
            message += f"<a href='{url}'>{json_item['title']}</a>\n\n"  # Link to the full article
            message += f"<span class ="tg-spoiler">{hover_description}</span>\n"  # Full description as italic
            message += f"新闻时间：<b>{json_item['date']}</b>"
            return message
        else:
            return f"<b>[{json_item['social_media']}]</b>：<a href=\"{json_item['url']}\">{json_item['title']}</a>"
    except Exception as e:
        logger.warning('消息格式化出现错误：',e)
        return  f"<b>[{e}]</b>"

# 主程序运行
if __name__ == "__main__":
    
    schedule.every(INTERVAL_TIME_NEWS).seconds.do(save_messages_to_redis)
    schedule.every(INTERVAL_TIME).seconds.do(push_news_hot_to_telegram)

    logger.info('程序启动成功！')

    while True:
        schedule.run_pending()
        time.sleep(1)
