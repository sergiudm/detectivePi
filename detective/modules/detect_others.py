import cv2
import time
from .common import is_sitting, is_slouching
from .common import check_status
import socket
import struct
import threading
import datetime

# from .device import activate_buzzer
# import RPi.GPIO as GPIO
import os
import time
from ..communication import send_email

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


def handle_detection(
    cap,
    path,
    pack_trans,
    server_email,
    server_password,
    smtp_server,
    smtp_port,
    target_email,
):
    output_path = os.path.join(path, "output_image.jpeg")
    success, img_output = cap.read()
    cv2.imwrite(output_path, img_output)
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
        with open("resources/test.png", "rb") as image_file:
            image_data = image_file.read()

        # 发送图片数据长度
        client_socket.sendall(len(image_data).to_bytes(4, byteorder="big"))

        # 发送图片数据
        client_socket.sendall(image_data)
        print("abbbbbbbbbb")
    else:
        current_time = datetime.datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        send_email(
            subject="国家反卷总局消息",
            body=f"<h1>来自 🤡🤡🤡🤡🤡</h1><p>国家反卷中心提示您，您的室友于{current_time}在内卷，请立即采取相应措施！下载[国家反卷中心APP](https://sergiudm.github.io/detective/)，查看更多信息！</p>",
            to_emails=target_email,
            from_email=server_email,
            password=server_password,
            smtp_server=smtp_server,
            smtp_port=smtp_port,
            image_path=output_path,  # Use the first image found
        )
        # 发邮件
    os.remove(output_path)
    print("Thread finished")


def working_detect(
    mpPose,
    pose,
    mpDraw,
    cap,
    image_path,
    protocol,
    pin,
    send_delay,
    effective_detection_duration,
    use_vis,
    pack_trans,
):
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
    try:
        model_1_time, model_1_state = 0, 0
        sitting_start_time = None
        slouching_start_time = None
        sitting = False
        slouching = False
        while True:
            success, img = cap.read()

            if not success:
                print("Error: Failed to read frame")
                break
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = pose.process(imgRGB)

            if results.pose_landmarks:
                # print("person detected!")
                mpDraw.draw_landmarks(
                    img, results.pose_landmarks, mpPose.POSE_CONNECTIONS
                )
                mpDraw.draw_landmarks(
                    img, results.pose_landmarks, mpPose.POSE_CONNECTIONS
                )
                for id, lm in enumerate(results.pose_landmarks.landmark):
                    h, w, c = img.shape
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
                landmarks = results.pose_landmarks.landmark

                sitting, sitting_start_time = check_status(
                    is_sitting,
                    landmarks,
                    mpPose,
                    sitting_start_time,
                    effective_detection_duration,
                )
                slouching, slouching_start_time = check_status(
                    is_slouching,
                    landmarks,
                    mpPose,
                    slouching_start_time,
                    effective_detection_duration,
                )

                working = sitting and slouching

                if sitting and model_1_time == 0:
                    model_1_time = time.time()
                    model_1_state = 1
                    detection_thread = threading.Thread(
                        target=handle_detection,
                        args=(
                            cap,
                            path,
                            pack_trans,
                            server_email,
                            server_password,
                            smtp_server,
                            smtp_port,
                            target_email,
                        ),
                    )
                    detection_thread.start()
                    print("Detection thread started")

                if time.time() - model_1_time > send_delay and model_1_state == 1:
                    model_1_state = 0
                    model_1_time = 0

                status_text = "Sitting" if sitting else "Not Sitting"
                j_text = ""
                if slouching:
                    j_text = "内卷！"

                cv2.putText(
                    img,
                    status_text,
                    (100, 100),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    3,
                    (0, 255, 0) if sitting else (0, 0, 255),
                    3,
                )

            cTime = time.time()
            fps = 1.0 / (cTime - pTime)
            pTime = cTime
            cv2.putText(
                img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3
            )

            if cv2.waitKey(1) == ord("q"):
                break
            if use_vis:
                cv2.imshow("Image", img)
            cv2.waitKey(1)

    except KeyboardInterrupt:
        cap.release()
        cv2.destroyAllWindows()
        print("Exit")
    finally:
        cap.release()
        cv2.destroyAllWindows()
