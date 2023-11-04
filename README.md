# 云盘版本2.1

- 完成UI界面设计
- 完成文件的存储、显示、下载、删除
- 完成用户的登录、登出、注册、删除、密码更改等，实现邮件验证
- 完成对象存储



# 部署

## 方案1 docker部署

#### 安装docker

##### 在linux系统上安装：

1. **更新软件包列表** 

   ```
   sudo apt-get update
   ```

2. **安装 Docker 的必要依赖**

   ```
   sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common
   ```

3. **添加 Docker 的官方 GPG 密钥**

   ```
   bashcurl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   ```

4. **设置稳定的存储库**

   ```
   bashsudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
   ```

5. **更新 apt 包索引、安装 Docker CE（社区版）**

   ```
   bashsudo apt-get update
   sudo apt-get install docker-ce docker-ce-cli containerd.io
   ```

6. **验证是否正确安装了 Docker**

   ```
   bashsudo docker run hello-world
   ```

##### mac系统

直接安装docker 的dmg应用程序

#### 部署docker镜像

> 当前版本为2.1，后续更新为latest

1. **拉取镜像**

   ```
   docker push xiaji2021/nis3368-cloud:2.1
   ```

2. **运行镜像**

   ```
   docker run -d -p <主机端口>:<容器监听端口> xiaji2021/nis3368-cloud:2.1
   ```

​		*`-d`参数表示后台运行*

访问`<主机ip> :主机端口` 即可





## 方案2 由源代码部署

> 在linux上部署

#### 下载源代码并解压

```
curl -LOk https://github.com/xiaji2021/NIS3368/archive/refs/heads/master.zip
```

```
sudo apt update
apt install unzip #确保安装unzip
unzip master.zip
cd NIS3368-master
```

#### 安装依赖

```
pip3 install -r requirements.txt
```

#### 运行项目

```
cd my_cloud
python3 manage.py runserver 0.0.0.0:8000
```

如需后台运行，使用nohup或screen

```
nohup python3 manage.py runserver 0.0.0.0:8000
```

**注意*，请确保8000端口未被占用且放行（防火墙规则设置）



