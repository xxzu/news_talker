# -*- coding: utf-8 -*-

import os
import sys
import time
import schedule
import json
from itertools import chain

from utils.ivs_log import LOGGER
# 定义日志配置
logger = LOGGER(logfile_name='push')
from news_pull_utils import *

from telegram_utils.sand_to_tg import send_to_telegram
from telegram_utils.send_to_financial_channel import send_to_financial_channel
from redis_server.redis_utils import RedisHandler
from dotenv import load_dotenv

load_dotenv()
REDIS_SERVER = os.getenv('REDIS_SERVER')
REDIS_PUSHED = os.getenv('REDIS_PUSHED')

##针对实时性很高要求的金融消息单独建立表格
REDIS_SERVER_FINANCIAL=os.getenv('REDIS_SERVER_FINANCIAL')
REDIS_PUSHED_FINANCIAL=os.getenv('REDIS_PUSHED_FINANCIAL')


INTERVAL_TIME_FETCH_NEWS = int(os.getenv('INTERVAL_TIME_FETCH_NEWS'))
INTERVAL_PUSH_TIME = int(os.getenv('INTERVAL_PUSH_TIME'))

## 金融消息推送
FINANCIAL_FETCH_TIME_NEWS = int(os.getenv('FINANCIAL_FETCH_TIME_NEWS'))
FINANCIAL_PUSH_TIME = int(os.getenv('FINANCIAL_PUSH_TIME'))


# 初始化 Redis 连接
redis_server = RedisHandler(set_key=REDIS_SERVER)
redis_pushed = RedisHandler(set_key=REDIS_PUSHED)


redis_financial_server = RedisHandler(set_key=REDIS_SERVER_FINANCIAL,default_ttl=3600)
redis_financial_pushed = RedisHandler(set_key=REDIS_PUSHED_FINANCIAL,default_ttl=7200)

def save_financial_messages_to_redis():
    try: 
        # gelonghui_news_list = fetch_gelonghui_news()
        jinsedata_news_list = fetch_jinse_news()
        for item in jinsedata_news_list:
            
            

            json_item = json.dumps(item)
            item_id = item.get('id')

            if redis_financial_pushed.is_in_set(str(item_id)):
                continue  # 跳过已推送的消息

            redis_financial_server.add_to_list(json_item)
       
    except Exception as e:
        logger.error(f"保存金融消息到 Redis 时发生错误: {e}")
        
def push_financial_messages_to_telegram():
    
    try:
        if redis_financial_server.get_list_length() != 0:
            item = redis_financial_server.loop_pop_messages()
            
            json_item = json.loads(item)
            # logger.info(f'消息推送：{json_item}')

            if not redis_financial_pushed.is_in_set(str(json_item['id'])):
                message = format_message(json_item)
                send_to_financial_channel(message)

                redis_financial_pushed.add_to_set(str(json_item['id']))

            time.sleep(2)  # 每条消息之间等待 3 秒
    except Exception as e:
        logger.error(f"推送消息时发生错误: {e}")



# 获取并存储热搜数据到 Redis
def save_messages_to_redis():
    try:
        baidu_news_list = get_baidu_hot_search()
        # bilibili_hot_list = get_bilibili_hot_search()
        # tieba_hot_list = get_baidu_tieba_hot_topics()
        zhihu_hot_list = get_zhihu_hot()
        # weibo_hot_list = fetch_weibo_hot_search()
        toutiao_hot_list = get_toutiao_hot()
        douyin_hot_list = fetch_douyin_hot_search()
        news36kr_hot_list = get_36kr_newsflashes()
        combined_news_hot_list = list(
                        chain(
                            zhihu_hot_list,
                            # weibo_hot_list, 
                            toutiao_hot_list,
                            # tieba_hot_list,
                            # bilibili_hot_list,
                            baidu_news_list,
                            douyin_hot_list,
                            news36kr_hot_list,
                           # fetch_cankaoxinxi_news(),
                            fetch_kaopu_news_data(),
                            fetch_zaobao_news(),
                            
                            
                            
                            ))
        
        # 用于跟踪已经记录的社交平台信息
        recorded_platforms = set()
        for item in combined_news_hot_list:
            recorded_platforms.add(item.get('social_media', ' '))
            

            json_item = json.dumps(item)
            item_id = item.get('id')

            if redis_pushed.is_in_set(str(item_id)):
                continue  # 跳过已推送的消息

            redis_server.add_to_set(json_item)
        logger.info(f"：{recorded_platforms}")
    except Exception as e:
        logger.error(f"保存消息到 Redis 时发生错误: {e}")

# 推送数据到 Telegram
def push_news_hot_to_telegram():
    
    try:
        if redis_server.get_set_length() != 0:
            item = redis_server.random_pop_messages()
            
            json_item = json.loads(item)
            logger.info(f'消息推送：{json_item}')

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
            hover_description = json_item['extra']['hover'][:200]
            url = json_item['url']
            
            # Full description in the message
            message = f"<b>[{json_item['social_media']}:{json_item['channelName']}]</b>:"
            # message += f"<b>{title}</b>\n"  # Title as bold
            message += f"<a href='{url}'>{json_item['title']}</a>\n"  # Link to the full article
            message += f"<blockquote expandable>{hover_description}</blockquote>\n"  # Full description as italic

            message += f"新闻时间：<b>{json_item['date']}</b>"
            return message
        elif json_item['social_media'] == '联合早报':
            # title = json_item['title']
            hover_description = json_item['description']
            url = json_item['url']
            
            # Full description in the message
            message = f"<b>[{json_item['social_media']}]</b>:"
            # message += f"<b>{title}</b>\n"  # Title as bold
            message += f"<a href='{url}'>{json_item['title']}</a>\n"  # Link to the full article
            message += f"<blockquote expandable>{hover_description}</blockquote>\n"  # Full description as italic

            message += f"新闻时间：<b>{json_item['date']}</b>"
            return message
        
        elif json_item['social_media'] == '格隆汇':
            # title = json_item['title']
            
            url = json_item['url']
            
            # Full description in the message
            message = f"<b>[{json_item['social_media']}:{json_item['info']}]</b>\n"
            # message += f"<b>{title}</b>\n"  # Title as bold
            message += f"<a href='{url}'>{json_item['title']}</a>\n"  # Link to the full article
            # message += f"<blockquote expandable>{hover_description}</blockquote>\n"  # Full description as italic

            message += f"<b>{json_item['date']}</b>"
            return message
        elif json_item['social_media'] == '金色财经':
            # title = json_item['title']
            
            url = json_item["url"]
            hover_description = json_item['description']
            # Full description in the message
            
            # message += f"<b>{title}</b>\n"  # Title as bold
            message = f"<a href='{url}'>{json_item['title']}</a>\n"  # Link to the full article
            message += f"{hover_description}\n"  # Full description as italic
            message += f"<b>[{json_item['social_media']}:{json_item['date']}]</b>"
            # message += f"情绪：<b>{json_item['emotions']}</b>\n"
            # message += f"<b>{json_item['date']}</b>"
            return message
        
        
        else:
            return f"<b>[{json_item['social_media']}]</b>：<a href=\"{json_item['url']}\">{json_item['title']}</a>"
    except Exception as e:
        logger.warning(f'消息格式化出现错误：{e}')
        return  f"<b>[{e}]</b>"

# 主程序运行
if __name__ == "__main__":
    
    schedule.every(INTERVAL_TIME_FETCH_NEWS).seconds.do(save_messages_to_redis)
    schedule.every(INTERVAL_PUSH_TIME).seconds.do(push_news_hot_to_telegram)
    schedule.every(FINANCIAL_FETCH_TIME_NEWS).seconds.do(save_financial_messages_to_redis)
    schedule.every(FINANCIAL_PUSH_TIME).seconds.do(push_financial_messages_to_telegram)


    logger.info('程序启动成功！')

    while True:
        schedule.run_pending()
        time.sleep(1)
