import requests
from utils.ivs_log import LOGGER
# 定义日志配置
logger = LOGGER()
def get_zhihu_hot():
    url = "https://www.zhihu.com/api/v3/feed/topstory/hot-lists/total?limit=20&desktop=true"
    try:
        # 发送 GET 请求
        response = requests.get(url)
        response.raise_for_status()  # 检查请求是否成功

        # 解析响应 JSON 数据
        data = response.json().get("data", [])

        # 格式化结果
        zhihu_hot_list = []
        for item in data:
            target = item.get("target", {})
            card_label = item.get("card_label", {})
            

            zhihu_hot_list.append({
                "social_media":"知乎",
                "id": target.get("id"),
                "title": target.get("title"),
                "icon": f"/api/proxy?img={card_label.get('night_icon')}" if card_label.get("night_icon") else None,
                "url": f"https://www.zhihu.com/question/{target.get('id')}",
            })

        return zhihu_hot_list

    except requests.RequestException as e:
        logger("获取知乎热点时发生错误:", e)
        return []
