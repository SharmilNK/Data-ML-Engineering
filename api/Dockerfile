# 使用轻量级 Python 镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件
COPY requirements.txt .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制源代码和 API 代码
# 注意：我们在构建镜像时，会把整个项目上下文传进去
COPY src/ ./src/
COPY api/ ./api/
COPY config/ ./config/
COPY models/ ./models/

# 暴露端口
EXPOSE 8000

# 启动命令
# 必须在 /app 目录下运行，这样 python path 才能找到 src
CMD ["uvicorn", "api.app:app", "--host", "0.0.0.0", "--port", "8000"]