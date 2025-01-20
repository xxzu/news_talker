import os
import time
import requests
from dotenv import load_dotenv
load_dotenv()
import os
TELEGRAM_CHANNEL_ID =  os.getenv("TELEGRAM_FINANCIAL_CHANNEL")
TELEGRAM_BOT_ID = os.getenv('FINANCIAL_CHANNEL_BOT')

from utils.ivs_log import LOGGER
# 定义日志配置
logger = LOGGER()

def send_to_financial_channel(message: str):
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_ID}/sendMessage"

    try:
        # print(f"Sending message to Telegram: {message}")  # 调试输出
        # 向 Telegram 发送消息
        response = requests.post(url, json={
            "chat_id": TELEGRAM_CHANNEL_ID,
            "text": message,
            "parse_mode": "HTML",
            "disable_web_page_preview": True  # 禁用链接预览
        })
        
        response_data = response.json()

        # 检查 Telegram 的响应
        if response_data.get('ok'):
            # print("Message sent successfully:", response_data)  # 显示成功信息
            # logger.info('send ok')
            pass
        else:
            # print("Error sending message:", response_data)
            if response_data.get('error_code') == 429:
                # 处理速率限制
                wait_time = response_data.get('parameters', {}).get('retry_after', 0)
                logger.error(f"Too many requests. Retrying after {wait_time} seconds...")
                time.sleep(wait_time)  # 等待指定的秒数
                return send_to_financial_channel(message)  # 重新发送消息
    except Exception as e:
        logger.error("发送消息到 Telegram 失败:", e)

# 示例调用
if __name__ == "__main__":
    send_to_financial_channel("Hello, Telegram!")
