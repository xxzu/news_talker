#!/bin/bash

# 设置镜像名称
IMAGE_NAME="pushnews_3"

# 1. 构建镜像
echo "Building Docker image..."
docker build -t $IMAGE_NAME .

# 2. 打包镜像为 tar 文件
echo "Saving Docker image to tar..."
docker save -o $IMAGE_NAME.tar $IMAGE_NAME

echo "Image built and saved successfully."
