import cv2
import mediapipe as mp
import time
from .common import is_sitting, is_slouching

# import RPi.GPIO as GPIO
# import smbus


def working_detect(mpPose, pose, mpDraw, cap, vis=True):
    pTime = 0
    try:
        while True:
            # 读取图像
            success, img = cap.read()
            if not success:
                print("Error: Failed to read frame")
                break
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

                # Display the result
                status_text = "Sitting" if is_sitting(landmarks) else "Not Sitting"
                j_test = is_slouching(landmarks) and is_sitting(landmarks)
                j_text = "neijuan" if j_test else "bu neijuan"
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
            cv2.imshow("Image", img)
            cv2.waitKey(1)
    except KeyboardInterrupt:
        cap.release()
        cv2.destroyAllWindows()
        print("Exit")
