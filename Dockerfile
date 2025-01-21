# 使用官方 Miniconda 镜像作为基础镜像
FROM continuumio/miniconda3

# 设置工作目录
WORKDIR /app

# 将当前目录下的所有文件复制到容器中的 /app 目录
COPY . .

# 使用 conda 创建并安装环境
RUN conda env create -f environment.yml

# 执行 conda init 来初始化 conda 环境
RUN conda init bash

# 激活 conda 环境并安装 pip 安装的其他依赖
RUN conda run -n news_talker pip install -r requirements.txt

# 设置默认的 shell 为 bash，并确保每次启动时激活 conda 环境
RUN echo "conda activate news_talker" >> ~/.bashrc

# 使用 bash 启动容器时，激活 conda 环境并启动应用
CMD ["bash", "-c", "source ~/.bashrc && python main_v1.1.1.py"]
