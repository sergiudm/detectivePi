import cv2
import mediapipe as mp
import time
from .common import is_sitting, is_slouching
#from .device import activate_buzzer
#import RPi.GPIO as GPIO
import os
import time 
from communication.mailbot import send_email
# import smbus

def get_path():
    # 获取当前文件的绝对路径
    current_file_path = os.path.abspath(__file__)

    # 获取当前文件的父文件夹路径
    parent_parent_directory = os.path.dirname(os.path.dirname(current_file_path))

    # 构建指向父文件夹中的 mailPic 目录的路径
    paths = os.path.join(parent_parent_directory, "resources")
    print(paths)
    return paths

def working_detect(mpPose, pose, mpDraw, cap, pin=None,path=get_path(),vis=True):
    # initial sensor pin
    #Pin_buzzer = 18
    #GPIO.setmode(GPIO.BCM)
    #GPIO.setup(Pin_buzzer, GPIO.OUT)
    print(path)
    pTime = 0
    try:
        model_1_time,model_1_state=0,0
        while True:
            # 读取图像
            success, img = cap.read()
            
            if not success:
                print("Error: Failed to read frame")
                break
            #save pic 
            output_path = os.path.join(path,'output_image.jpeg').replace('\\', '/')
            # modify the first letter of the path to be upper case
            output_path = output_path[0].upper() + output_path[1:]
            print('output_path:',output_path)
            result = cv2.imwrite(output_path, img)
            print(result)                
            
            if result:
                print(f"Image saved successfully as {output_path}.")
            else:
                print(f"Failed to save the image to {output_path}.")
                # 检查具体原因
                if not os.access(path, os.W_OK):
                    print("Permission denied: Unable to write to the directory.")
                elif not os.path.isdir(path):
                    print("Invalid path: The specified path is not a directory.")
                else:
                    print("Unknown error occurred during file writing.")


            print('111111111111111')
            # 转换为RGB格式，因为Pose类智能处理RGB格式，读取的图像格式是BGR格式
            imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            # 处理一下图像
            results = pose.process(imgRGB)
            # print(results.pose_landmarks)
            # 检测到人体的话：
            if results.pose_landmarks:
                # 使用mpDraw来刻画人体关键点并连接起来
                mpDraw.draw_landmarks(img, results.pose_landmarks, mpPose.POSE_CONNECTIONS)
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
                sitting = is_sitting(landmarks)

                ####
                #创建一个新的线程来检测检测时间
                if sitting and model_1_time==0: #检测特定手势(model_1)
                    #如果是
                    model_1_time = time.time()
                    model_1_state = 1
                    #image_files = [f for f in os.listdir(path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.gif'))]
                    #first_image_path = os.path.join(path, image_files[0])
                    
                    send_email(
                        subject="Test Email",
                        body="<h1>This is a test email for 🤡🤡🤡🤡🤡</h1><p>With an image attached below.</p>",
                        to_emails=["2824174663@qq.com", "12212635@mail.sustech.edu.cn"],
                        from_email="2990973166@qq.com",
                        password="xfmhwdmoutajdhed",
                        smtp_server="smtp.qq.com",
                        smtp_port=587,
                        image_path=output_path  # Use the first image found
                    )
                    #发邮件
                if time.time()-model_1_time>13 and model_1_state==1:
                    model_1_state = 0
                    model_1_time = 0
                #10秒后解封
                ####

                # Display the result
                status_text = "Sitting" if sitting else "Not Sitting"
                j_test = is_slouching(landmarks) and is_sitting(landmarks)
                j_text = "neijuan" if j_test else "bu neijuan"


                #activate sensor
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
            pTime = cTime
            cv2.putText(
                img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3
            )

                # 按'q'退出循环
            if cv2.waitKey(1) == ord('q'):
                break

            cv2.imshow("Image", img)
            os.remove(output_path)
            cv2.waitKey(100)
        
        # 释放摄像头资源
        cap.release()
        # 关闭所有OpenCV窗口
        cv2.destroyAllWindows()
    except KeyboardInterrupt:
        cap.release()
        cv2.destroyAllWindows()
        print("Exit")
