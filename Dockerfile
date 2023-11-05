# 设置基础镜像
FROM python:3.8

# 将工作目录切换到 /app
WORKDIR /app

# 复制 requirements.txt 文件到容器中
COPY requirements.txt .

# 安装依赖库
RUN pip install --no-cache-dir -r requirements.txt

# 复制整个 Django 项目到容器中
COPY . /app

# 配置环境变量等
ENV DJANGO_SETTINGS_MODULE=my_cloud.settings

RUN rm ./my_cloud/db.sqlite3
RUN python3 ./my_cloud/manage.py makemigrations
RUN python3 ./my_cloud/manage.py migrate

# 运行 Django 项目
CMD ["python3", "./my_cloud/manage.py", "runserver", "0.0.0.0:8000"]
