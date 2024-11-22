import cv2
import mediapipe as mp
import time
from .common import is_sitting, is_slouching
import socket
import struct

# from .device import activate_buzzer
# import RPi.GPIO as GPIO
import os
import time
from communication.mailbot import send_email

# import smbus


def get_path(parent_path):
    # 获取当前文件的绝对路径
    current_file_path = os.path.abspath(__file__)

    # 获取当前文件的父文件夹路径
    parent_parent_directory = os.path.dirname(os.path.dirname(current_file_path))

    # 构建指向父文件夹中的 mailPic 目录的路径
    paths = os.path.join(parent_parent_directory, parent_path)
    print(paths)
    return paths


def working_detect(mpPose, pose, mpDraw, cap, image_path, protocol, pin, use_vis,pack_trans):
    # initial sensor pin
    # Pin_buzzer = pin
    # GPIO.setmode(GPIO.BCM)
    # GPIO.setup(Pin_buzzer, GPIO.OUT)
    path = get_path(image_path)
    server_email = protocol[0]
    server_password = protocol[1]
    smtp_server = protocol[2]
    smtp_port = int(protocol[3])
    target_email = protocol[4]
    pTime = 0
    if_save = 0
    try:
        model_1_time, model_1_state = 0, 0
        while True:
            #while cap.isOpened() and cap.grab():
            #    print("iii")
            #    pass
            # 读取图像
            while cap.isOpened() and cap.grab():
                pass
            success, img = cap.read()

            if not success:
                print("Error: Failed to read frame")
                break
            # save pic
            output_path = os.path.join(path, "output_image.jpeg")
            # cv2.imwrite(output_path, img)
            # 转换为RGB格式，因为Pose类智能处理RGB格式，读取的图像格式是BGR格式
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # 处理一下图像
            results = pose.process(imgRGB)
            # print(results.pose_landmarks)
            # 检测到人体的话：
            if results.pose_landmarks:
                print("person detected!")
                # 使用mpDraw来刻画人体关键点并连接起来
                mpDraw.draw_landmarks(
                    img, results.pose_landmarks, mpPose.POSE_CONNECTIONS
                )
                mpDraw.draw_landmarks(
                    img, results.pose_landmarks, mpPose.POSE_CONNECTIONS
                )
                # 如果我们想对33个关键点中的某一个进行特殊操作，需要先遍历33个关键点
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    # 打印出来的关键点坐标都是百分比的形式，我们需要获取一下视频的宽和高
                    h, w, c = img.shape
                    # print(id, lm)
                    # 将x乘视频的宽，y乘视频的高转换成坐标形式
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    # 使用cv2的circle函数将关键点特殊处理
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                landmarks = results.pose_landmarks.landmark

                # Check if the person is sitting
                sitting = is_sitting(landmarks, mpPose=mpPose)
                if sitting :print("sitting!")  
                slouching = is_slouching(landmarks, mpPose=mpPose)
                working = sitting and slouching

                ####
                # 创建一个新的线程来检测检测时间
                if sitting and model_1_time == 0:  # 检测特定手势(model_1)
                    # 如果是
                    model_1_time = time.time()
                    model_1_state = 1
                    # image_files = [f for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                    # first_image_path = os.path.join(path, image_files[0])
                    success, img_output = cap.read()
                    cv2.imwrite(output_path, img_output)
                    if_save = 1
                    print("aaaaaaaaaa")
                    if pack_trans:
                        # 设置服务器的IP地址和端口号
                        server_ip = "10.13.220.234"  # 替换X为服务器的实际IP地址
                        server_port = 12345

                        # 创建一个socket对象
                        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        print(11234)
                        # 连接到服务器
                        client_socket.connect((server_ip, server_port))
                        print(4322)
                    
                        # 创建一个8位的布尔数组
                        bool_array = [1, 0, 0, 1, 0, 0, 1, 0]  # 示例数组

                        # 将布尔数组打包成一个字节
                        packed_data = struct.pack("B", int("".join(map(str, bool_array)), 2))

                        # 发送数据到服务器
                        client_socket.sendall(packed_data)
                        print("abbbbbbbbbb")
                    else:
                        print(987987)
                        send_email(
                            subject="国家反卷总局消息",
                            body="<h1>来自 🤡🤡🤡🤡🤡</h1><p>With an image attached below.</p>",
                            to_emails=["2824174663@qq.com", "12212635@mail.sustech.edu.cn"],
                            from_email=server_email,
                            password=server_password,
                            smtp_server=smtp_server,
                            smtp_port=smtp_port,
                            #image_path=output_path,  # Use the first image found
                        )
                        # 发邮件
                if time.time() - model_1_time > 13 and model_1_state == 1:
                    model_1_state = 0
                    model_1_time = 0
                # 10秒后解封
                ####

                # Display the result

                status_text = "Sitting" if sitting else "Not Sitting"
                j_text = "neijuan" if working else "bu neijuan"

                # activate sensor
                # if sitting:
                #     activate_buzzer(pin, GPIO.HIGH)
                # else:
                #     activate_buzzer(pin, GPIO.LOW)

                cv2.putText(
                    img,
                    status_text,
                    (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    3,
                    (0, 255, 0) if sitting else (0, 0, 255),
                    3,
                )

                # cv2.putText(
                #     img,
                #     j_text,
                #     (150, 100),
                #     cv2.FONT_HERSHEY_SIMPLEX,
                #     3,
                #     (0, 255, 0) if sitting else (0, 0, 255),
                #     3,
                # )

            # 计算fps值
            cTime = time.time()
            fps = 1.0 / (cTime - pTime)
            #print(fps) 
            pTime = cTime
            cv2.putText(
                img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3
            )

            # 按'q'退出循环
            if cv2.waitKey(1) == ord("q"):
                break
            if use_vis:
                cv2.imshow("Image", img)
            if if_save == 1:
                os.remove(output_path)
                if_save = 0
            cv2.waitKey(1)

        # 释放摄像头资源
        cap.release()
        # 关闭所有OpenCV窗口
        cv2.destroyAllWindows()
    except KeyboardInterrupt:
        cap.release()
        cv2.destroyAllWindows()
        print("Exit")
