import cv2
import mediapipe as mp
from .common import detect_all_finger_state, detect_hand_state

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(
    static_image_mode=False,
    max_num_hands=2,
    min_detection_confidence=0.65,
    min_tracking_confidence=0.65,
)


def show_message(frame, message, position=(10, 30)):
    cv2.putText(
        frame,
        message,
        position,
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (0, 255, 0),
        2,
        cv2.LINE_AA,
    )


recent_states = [""] * 20


def gesture_detect(cap):
    """detect hand gesture"""
    while True:
        ret, frame = cap.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w = frame.shape[:2]
        frame = cv2.flip(frame, 1)  # flip the frame horizontally
        results = hands.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        if results.multi_handedness:
            for hand_label in results.multi_handedness:
                # print(hand_label)
                pass
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # print("hand_landmarks:", hand_landmarks)
                # landmarks visualization
                mp_drawing.draw_landmarks(
                    frame, hand_landmarks, mp_hands.HAND_CONNECTIONS
                )
                # gesture recognition
                lm = results.multi_hand_landmarks[0]
            lmHand = mp_hands.HandLandmark

            landmark_list = [
                [] for _ in range(6)
            ]  # landmark_list有 6 个子列表，分别存储着根节点坐标（0点）以及其它 5 根手指的关键点坐标

            for index, landmark in enumerate(lm.landmark):
                x = int(landmark.x * w)
                y = int(landmark.y * h)
                if index == lmHand.WRIST:
                    landmark_list[0].append((x, y))
                elif 1 <= index <= 4:
                    landmark_list[1].append((x, y))
                elif 5 <= index <= 8:
                    landmark_list[2].append((x, y))
                elif 9 <= index <= 12:
                    landmark_list[3].append((x, y))
                elif 13 <= index <= 16:
                    landmark_list[4].append((x, y))
                elif 17 <= index <= 20:
                    landmark_list[5].append((x, y))

            # 获取所有关节点的坐标
            point0 = landmark_list[0][0]
            point1, point2, point3, point4 = (
                landmark_list[1][0],
                landmark_list[1][1],
                landmark_list[1][2],
                landmark_list[1][3],
            )
            point5, point6, point7, point8 = (
                landmark_list[2][0],
                landmark_list[2][1],
                landmark_list[2][2],
                landmark_list[2][3],
            )
            point9, point10, point11, point12 = (
                landmark_list[3][0],
                landmark_list[3][1],
                landmark_list[3][2],
                landmark_list[3][3],
            )
            point13, point14, point15, point16 = (
                landmark_list[4][0],
                landmark_list[4][1],
                landmark_list[4][2],
                landmark_list[4][3],
            )
            point17, point18, point19, point20 = (
                landmark_list[5][0],
                landmark_list[5][1],
                landmark_list[5][2],
                landmark_list[5][3],
            )

            # 将所有关键点的坐标存储到一起，简化后续函数的参数
            all_points = {
                "point0": landmark_list[0][0],
                "point1": landmark_list[1][0],
                "point2": landmark_list[1][1],
                "point3": landmark_list[1][2],
                "point4": landmark_list[1][3],
                "point5": landmark_list[2][0],
                "point6": landmark_list[2][1],
                "point7": landmark_list[2][2],
                "point8": landmark_list[2][3],
                "point9": landmark_list[3][0],
                "point10": landmark_list[3][1],
                "point11": landmark_list[3][2],
                "point12": landmark_list[3][3],
                "point13": landmark_list[4][0],
                "point14": landmark_list[4][1],
                "point15": landmark_list[4][2],
                "point16": landmark_list[4][3],
                "point17": landmark_list[5][0],
                "point18": landmark_list[5][1],
                "point19": landmark_list[5][2],
                "point20": landmark_list[5][3],
            }

            # 调用函数，判断每根手指的弯曲或伸直状态
            bend_states, straighten_states = detect_all_finger_state(all_points)

            # 调用函数，检测当前手势
            current_state = detect_hand_state(
                all_points, bend_states, straighten_states
            )

            # 更新最近状态列表
            recent_states.pop(0)
            recent_states.append(current_state)

            # 检查列表中的所有状态是否相同
            if (
                len(set(recent_states)) == 1
            ):  # 如果连续30帧的手势状态都相同，则认为手势稳定，输出当前手势
                print("Detected consistent hand state:", recent_states[0])
                cv2.putText(
                    frame,
                    current_state,
                    (10, 70),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    1,
                    (0, 0, 255),
                    2,
                    cv2.LINE_AA,
                )

            for (
                hand_landmarks
            ) in (
                results.multi_hand_landmarks
            ):  # results.multi_hand_landmarks是一个列表，只有一个元素，存储着21个关键点的xyz坐标。使用for循环遍历
                mp_drawing.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing.DrawingSpec(
                        color=(0, 255, 0), thickness=2, circle_radius=4
                    ),
                    mp_drawing.DrawingSpec(
                        color=(255, 0, 0), thickness=2, circle_radius=2
                    ),
                )

        cv2.imshow("MediaPipe Hands", frame)
        if cv2.waitKey(1) & 0xFF == 27:
            break
    cap.release()
