### 一个新闻推送工具
主要是使用python对新闻热点进行推送，推送到tg频道统一查看，打破信息壁垒
##### TODO
- [ ] 实现金融消息的推送
- [ ] 实现科技消息的推送
- [x] 国内平台热点消息推送
##### 已包含平台
| 平台热点    | 科技热点 | 金融热点 ->实时  |
|:-------------|:---------:|:-----------:|
| - [x] 百度  | 酷安  | 华尔街见闻  |
| - [x] 贴吧  | hacker news   | 联合早报 |
| - [x] 头条  | product hunt   | IT之家      |
| - [x] 哔哩  | github | 财联社|
| - [x] 参考消息|       | 格隆汇|
|- [x] 36kr|         |   金十数据|
|- [x] 微博|
|- [x] 知乎|
|- [x] kaopu|
|- [x] 抖音|
###### docker 构建
首先创建基于项目的环境配置文件 
1.pip安装环境 pip freeze > requirement.txt
2.conda 安装环境 conda env export --no-builds > environment.yml
3.从这两个环境中构建docker image  -》docker build -t images_names:v1
请注意保持conda环境名称一致性
保存构建的image :_> docker save pushnews:v1 > pushnews_v1.tar
docker-compose构建.yml的时候时需要将redis_host的端口指向redis