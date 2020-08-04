# 部署指南

## 下载Pekobot代码

```bash
mkdir apps
cd apps
https://github.com/Marchen-Kingdom/pekobot.git
```

## 配置Pekobot

```bash
cp pekobot-config-example-yaml pekobot-config.yaml
vim pekobot-config.yaml
cd -
```

## Python

```bash
curl -L https://github.com/pyenv/pyenv-installer/raw/master/bin/pyenv-installer | bash
pyenv install 3.8.3
pyenv shell 3.8.3
cd apps/pekobot
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

## 启动Pekobot

```bash
sudo apt install -y node npm
npm install -g pm2
pm2 start pm2.json
pm2 start pekobot
```
