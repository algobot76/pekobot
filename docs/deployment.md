# 部署指南

## 申请Discord机器人

在部署佩可机器人之前，需要去Discord官网申请一个机器人。具体操作请参考[这篇教程](https://discordpy.readthedocs.io/en/latest/discord.html)。

## 安装PM2

[PM2](https://pm2.keymetrics.io/)是个开源的进程管理工具。我们用PM2来管理佩可机器人的进程。

### Ubuntu

```bash
sudo apt update
sudo apt install node npm
npm install -g pm2
```

## 安装Python

### Ubuntu

```bash
sudo apt update
sudo apt install make build-essential libssl-dev zlib1g-dev libbz2-dev libreadline-dev libsqlite3-dev wget curl llvm libncurses5-dev xz-utils tk-dev libxml2-dev libxmlsec1-dev libffi-dev liblzma-dev
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
exec $SHELL
pyenv install 3.8.3
```

## 安装机器人的依赖

### Ubuntu

```bash
mkdir apps
cd apps
git clone https://github.com/Marchen-Kingdom/pekobot.git
cd pekobot
pyenv shell 3.8.3
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## 启动机器人

```bash
pm2 start pm2.json
```
