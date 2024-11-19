import cv2

# 初始化摄像头
cap = cv2.VideoCapture(0)  # 参数0通常表示默认的摄像头

# 检查摄像头是否成功打开
if not cap.isOpened():
    print("无法打开摄像头")
    exit()

# 循环读取摄像头的每一帧
while True:
    # 读取一帧图像
    ret, frame = cap.read()

    # 如果正确读取帧，ret为True
    if not ret:
        print("无法读取帧")
        break

    # 显示图像
    cv2.imshow('摄像头', frame)

    # 按'q'退出循环
    if cv2.waitKey(1) == ord('q'):
        break

# 释放摄像头资源
cap.release()
# 关闭所有OpenCV窗口
cv2.destroyAllWindows()