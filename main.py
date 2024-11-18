import cv2
import mediapipe as mp
import math
import time

# 两个初始化
mpPose = mp.solutions.pose
pose = mpPose.Pose()
# 初始化画图工具
mpDraw = mp.solutions.drawing_utils

# 调用摄像头，在同级目录下新建videos文件夹，然后在里面放一些MP4文件，方便读取
cap = cv2.VideoCapture("assets/videos/sit.mp4")
if not cap.isOpened():
    print("Error: Cannot open video file")
    exit()

# 计算pfs值需要用到的变量，先初始化以一下
pTime = 0


def is_sitting(landmarks):
    left_hip = landmarks[mpPose.PoseLandmark.LEFT_HIP.value]
    left_knee = landmarks[mpPose.PoseLandmark.LEFT_KNEE.value]
    left_ankle = landmarks[mpPose.PoseLandmark.LEFT_ANKLE.value]

    # Calculate angle at the left knee
    angle = calculate_angle(left_hip, left_knee, left_ankle)

    if angle < 140:
        return True
    else:
        return False


def calculate_angle(a, b, c):
    a = [a.x, a.y]
    b = [b.x, b.y]
    c = [c.x, c.y]

    ab = [a[0] - b[0], a[1] - b[1]]
    cb = [c[0] - b[0], c[1] - b[1]]

    dot_product = ab[0] * cb[0] + ab[1] * cb[1]
    ab_magnitude = math.hypot(ab[0], ab[1])
    cb_magnitude = math.hypot(cb[0], cb[1])

    angle = math.acos(dot_product / (ab_magnitude * cb_magnitude))
    return math.degrees(angle)


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
            print(id, lm)
            # 将x乘视频的宽，y乘视频的高转换成坐标形式
            cx, cy = int(lm.x * w), int(lm.y * h)
            # 使用cv2的circle函数将关键点特殊处理
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)
        landmarks = results.pose_landmarks.landmark

        # Check if the person is sitting
        sitting = is_sitting(landmarks)

        # Display the result
        status_text = "Sitting" if is_sitting(landmarks) else "Not Sitting"
        cv2.putText(
            img,
            status_text,
            (100, 100),
            cv2.FONT_HERSHEY_SIMPLEX,
            3,
            (0, 255, 0) if sitting else (0, 0, 255),
            3,
        )

    # 计算fps值
    cTime = time.time()
    fps = 1.0 / (cTime - pTime)
    pTime = cTime
    cv2.putText(img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)
    cv2.imshow("Image", img)
    cv2.waitKey(1)
