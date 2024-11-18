detective：一款更适合中国宝宝的室友内卷监测工具
==================================================

## 1. 介绍

detective是一款更适合中国宝宝的室友内卷监测工具，它可以帮助你监测室友的内卷行为，让你的室友生活更加和谐。

## 2. 安装依赖
    
```bash
pip install -r requirements.txt
```

## 3. 使用说明

```bash
git clone https://github.com/sergiudm/detective.git
cd detective
python3 main.py
```

## 4. 功能
- 检测是否有室友在内卷
    - 如果有，会自动响起警报，并且发微信通知你
- 检测你是不是卷过头了
    - 如果连续工作超过2小时（可在`config.json`中配置），会自动响起警报，并提醒你休息一下
