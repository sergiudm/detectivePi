Thread-Everything: 一个简单易用的跨平台多端通信工具
==================================================
[![Deploy MkDocs site to GitHub Pages (using mkdocs gh-deploy)](https://github.com/sergiudm/detectivePi/actions/workflows/mkdocs.yml/badge.svg)](https://github.com/sergiudm/detectivePi/actions/workflows/mkdocs.yml)
[![CI Tests](https://github.com/sergiudm/detectivePi/actions/workflows/test.yml/badge.svg)](https://github.com/sergiudm/detectivePi/actions/workflowstest.yml)
[![PyPI version](https://badge.fury.io/py/detective-pi.svg)](https://pypi.org/project/detective-pi/0.2.0/)
![GitHub license](https://img.shields.io/github/license/sergiudm/detectivePi)
## 介绍

Thread-Everything 提供了一个简单的 API，可以集成来自*不同*主机的任何Python线程（插件,它可以帮助您更有效地管理线程和通信。

例如：
- 使用单个 Windows 客户端控制远程机器人。
- 与朋友一起使用手势玩在线游戏。
- 使用单个服务器监控您的家。


## 环境要求
| 环境   | 版本                         |
| ------ | ---------------------------- |
| OS     | Ubuntu22.04, Raspberry Pi OS, Window11, Debian 12|
| Python | 3.10                         |

## 硬件清单
- Raspberry Pi 4B * 2
- 摄像头 * 2
- 蜂鸣器
- LED灯
- 面包板

## 安装
## pip安装
```bash
pip install detective-pi
```

## 源码安装
克隆仓库
```bash
git clone https://github.com/sergiudm/detective.git
cd detective
```
你可以使用`deploy.sh`脚本自动安装
```bash
sudo chmod +x deploy.sh
./deploy.sh
```
或者手动安装
```bash
conda create -n <your_env_name> python=3.10
conda activate <your_env_name>
pip install -r requirements.txt
```

## 使用说明
开始前，你需要配置在项目根目录创建一个`config.json`文件，
以下是一个示例：
```json
{
    "use_pi": false,
    "plugin_list": [
        "information_server",
        "GPIO_controller",
        "music_server",
        "gpio_controller",
        "gesture_detection",
        "meditation_helper",
    ], # 注意：涉及GPIO的插件要开启`use_pi`，如果不使用GPIO相关的库则关闭
    "default_detect_mode": "others",
    "use_camera": true,
    "LED_pin": 18, # LED灯的引脚
    "use_visualization": false, # 是否使用可视化
    "server_email": "youremail@example.com",
    "server_email_password": "your email password",# 请使用授权码
    "target_email": [
        "email1",
        "email2"
    ],
    "smtp_server":"your smtp server",
    "smtp_port": 587,
    "video_path": "assets/videos/sit.mp4", # use_camera为false时，使用该视频
    "image_path": "resources", # 邮件中的图片
    "send_delay": 13,
    "effective_detection_duration": 2,
    "max_num_hands": 2,
    "min_detection_confidence": 0.65,
    "min_tracking_confidence": 0.65,
    "pin_data": {
        "pin_list": [
            17,
            23,
            24,
            25,
            27
        ],
        "pin_map": {
            "Right": [
                17,
                23,
                24
            ],
            "Return": [
                23,
                24
            ],
            "Left": [
                17,
                24
            ],
            "Pause": [],
            "Like": [
                25
            ],
            "OK": [
                27
            ]
        }
    }
}
```
>[!CAUTION] 
实际使用时，请删除`config.json`中的所有注释!

Linux:
```bash
sudo chmod +x run.sh
./run.sh
```
Windows:
```bash
./win_run.bat
```

## 功能
- 手势检测
    - 开启手势线程之后，计算机使用搭载的摄像头捕捉图像信息，并分析画面中的手势，如“OK”、“Like”等。
    - 会反馈当前的手势信息。
- 姿势检测
    - 开启姿势线程之后，计算机使用搭载的摄像头捕捉图像信息，并分析画面中的人体姿势，如“sitting”、“slouching”等。
    - 会反馈当前的姿势信息。
- 音乐控制
    - 音乐线程可以控制设备上的音乐流。
    - 该线程需要信息的输入，如：通过命令行输入、手势线程的输入。 
    - 将音乐文件放入指定路径，音乐线程即可自动控制。
- GPIO控制
    - GPIO控制线程只能在树莓派上使用，用于控制GPIO引脚的电平。
    - 该线程需要信息的输入，如：通过命令行输入、手势线程的输入。
- 个性化邮件发送
    - GPIO控制线程只能在树莓派上使用，用于控制GPIO引脚的电平。
    - 该线程需要信息的输入，如：通过命令行输入、手势线程的输入。



## 应用场景


- 冥想助手
    - 应用场景的假设：用户希望在冥想开启时与冥想中不被工作琐事干扰，如电话、微信等。现阶段的计时器（番茄钟）需要使用手机或者闹钟进行接触式的时间设定，并无法观测用户的姿势是否正确。使用Thread-Everything 实现的冥想助手可以进行无接触式的时间设定与姿势校正提示。
    - 用户使用手势设定冥想时间，并进行冥想。
    - 冥想过程中，树莓派会使用摄像头监控人体姿势，如发现姿势不正确，就会发送提示邮件，提醒用户校正姿势。



- to do list
  - 检测 学习 与 玩游戏
    - 肩部、髋部、膝盖 夹角； 手部 位置
  - 报警：蜂鸣器（可换为便宜的喇叭）（直到结束学习才消失）、led、微信发消息
  - 开关门检测
    - 开关门 检测完成后： 人在寝室，才监控
  - 不良坐姿的检测
  - 魔术

## 如何贡献
本仓库仅使用了[mediapipe](https://github.com/google-ai-edge/mediapipe)中的人体姿态检测和手部检测功能，如果你有更多想法，欢迎：

- 提交PR
  - [插件指南]()
- 提交Issue
- 传播给更多的室友

## Acknowledgement
[mediapipe](https://github.com/google-ai-edge/mediapipe)