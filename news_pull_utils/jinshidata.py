# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, timezone
from typing import List, Dict
from utils.ivs_log import LOGGER
import re
# 定义日志配置
logger = LOGGER()

def parse_relative_date(relative_time: str, timezone: str = "Asia/Shanghai") -> int:
    # 模拟解析相对时间的函数。需要根据实际需求调整。
    if "分钟前" in relative_time:
        minutes = int(relative_time.replace("分钟前", "").strip())
        return int((datetime.now() - timedelta(minutes=minutes)).timestamp() * 1000)
    elif "小时前" in relative_time:
        hours = int(relative_time.replace("小时前", "").strip())
        return int((datetime.now() - timedelta(hours=hours)).timestamp() * 1000)
    elif "天前" in relative_time:
        days = int(relative_time.replace("天前", "").strip())
        return int((datetime.now() - timedelta(days=days)).timestamp() * 1000)
    else:
        # 默认返回当前时间戳
        return int(datetime.now().timestamp() * 1000)

import time
def get_time():
   
    # current_time = datetime.now()
    
    # 时间戳（毫秒）
    # timestamp_s = datestamp / 1000  # 转换为秒
    

# 获取当前时间戳
    timestamp_s = time.time()

    # # 输出时间戳
    # print("当前时间戳:", timestamp)

    date = datetime.fromtimestamp(timestamp_s, timezone.utc)

    # 转换为本地时间
    local_time = date.astimezone(timezone(timedelta(hours=8)))  # UTC+8
    formatted_date = local_time.strftime("%Y-%m-%d ")
    return formatted_date


def fetch_jinse_news() -> List[Dict]:
    try:
        # 基础 URL
        base_url = "https://www.jinse.cn"

        # 发起请求
        response = requests.get(f"{base_url}/lives/")
        response.raise_for_status()  # 检查请求是否成功

        # 使用 BeautifulSoup 解析 HTML
        soup = BeautifulSoup(response.text, "html.parser")

        # 定位主要内容
        main_content = soup.select("div.js-lives__item")  # 使用 CSS 选择器
        news_list = []

        for element in main_content:
            # 提取标题
            a_tag = element.select_one("a.title")
            title = a_tag.text.strip() if a_tag else "无标题"

            # 提取链接
            link = base_url + a_tag["href"] if a_tag and "href" in a_tag.attrs else "无链接"

            # 提取时间（假设时间在特定 class 中）
            time_tag = element.select_one(".time")
            
            
            # news_time = time_tag.text.strip() if time_tag else "无时间"
            if time_tag :
                news_time = get_time() +" " + time_tag.text.strip() 
            
            else:
                news_time = "无时间"
                

            # 提取描述
            

            description = element.select_one('div.content > a:nth-of-type(2)').text.strip()
            # description = element.select_one('div.content > a:nth-of-type(2)').text.strip().replace('【' + title +'】',"")
            description = re.sub(r"【" + re.escape(title) + "】", "", description)  # 使用正则去掉标题部分
            # Extract "利好" (positive)
            positive = element.select_one('a.like.rose-h').text.strip() if element.select_one('a.like.rose-h') else "无利好"

            # Extract "利空" (negative)
            negative = element.select_one('a.like.fall').text.strip() if element.select_one('a.like.fall') else "无利空"

            # 添加到列表
            news_list.append({
                'social_media':"金色财经",
                "date": news_time,
                "title": title,
                "description": description,
                "url": link,
                "emotions": f"[{positive}] [{negative}]",
                'id':link
            })

        return news_list

    except requests.RequestException as e:
        logger.error(f"请求失败: {e}")
        return []


# 调用函数并打印结果
if __name__=="__main__":
    news = fetch_jinse_news()
    # for item in news:
    #     print(f"时间: {item['time']}")
    #     print(f"标题: {item['title']}")
    #     print(f"描述: {item['description']}")
    #     print(f"链接: {item['link']}")
    #     print(f"情绪: {item['emotions']}")
    #     print("-" * 40)
    print(f'{news}')
