detective：一款更适合中国宝宝的室友内卷监测工具
==================================================

## 介绍

detective是一款更适合中国宝宝的室友内卷监测工具，它可以帮助你监测室友的内卷行为，让你的寝室生活更加和谐。
> TODO：demo

## 环境要求
| 环境   | 版本                         |
| ------ | ---------------------------- |
| OS     | Ubuntu22.04, Raspberry Pi OS |
| Python | 3.12                         |

## 安装依赖
创建虚拟环境
```bash
conda create -n your_env_name python=3.12
conda activate your_env_name
```
安装依赖
```bash
git clone https://github.com/sergiudm/detective.git
cd detective
pip install -r requirements.txt
```

## 使用说明

```bash
cd detective
python3 main.py
```

## 功能
- 检测是否有室友在内卷
    - 如果有，会自动响起警报，并且发微信通知你
- 检测你是不是卷过头了
    - 如果连续工作超过2小时（可在`config.json`中配置），会自动响起警报，并提醒你休息一下

## 如何贡献

- 提交PR
- 提交Issue
- 传播给更多的室友

## Acknowledgement
[mediapipe](https://github.com/google-ai-edge/mediapipe)