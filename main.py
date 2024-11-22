import cv2
import mediapipe as mp

from modules import *
from modules import working_detect, relax_detect
from modules import Config


# initializations
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils


# Use the parsed configuration
config = Config()
LED_pin = config.get_param("LED_pin")
detect_other = config.get_param("default_detect_mode") == "others"
use_camera = config.get_param("use_camera")
video_path = config.get_param("video_path")
image_path = config.get_param("image_path")
server_email = config.get_param("server_email")
server_password = config.get_param("server_email_password")
smtp_server = config.get_param("smtp_server")
smtp_port = config.get_param("smtp_port")
target_email = config.get_param("target_email")
protocol = [server_email, server_password, smtp_server, smtp_port, target_email]
use_vis = config.get_param("use_visualization")
packet_transfer = config.get_param("packet_tansfer")#true: windows
print(packet_transfer)
print("Configuration:")
config.print_info()

# setup path
if use_camera:
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)


else:
    cap = cv2.VideoCapture(video_path)

if not cap.isOpened():
    print("Error: Cannot open video file")
    exit()

# Further code to use default_detect_mode
# q --- quit the program
if detect_other:
    working_detect(
        mpPose, pose, mpDraw, cap, image_path=image_path,
          protocol=protocol, pin=LED_pin, use_vis=use_vis,pack_trans=packet_transfer
    )
else:
    relax_detect(mpPose, pose, mpDraw, cap)
