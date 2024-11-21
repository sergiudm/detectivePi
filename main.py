import cv2
import mediapipe as mp

#import RPi.GPIO as GPIO
# import smbus
from modules import *
from modules import working_detect, relax_detect
from modules import parse_json

  # initial sensor pin
Pin_buzzer = 18
# GPIO.setmode(GPIO.BCM)
# GPIO.setup(Pin_buzzer, GPIO.OUT)


# initializations
mpPose = mp.solutions.pose
pose = mpPose.Pose()
mpDraw = mp.solutions.drawing_utils
# GPIO setup
# GPIO.setmode(GPIO.BCM)
# TODO

config = parse_json("config.json")

# Use the parsed configuration
detect_other = config.get("default_detect_mode", "others") == "others"
use_camera = config.get("use_camera", True)
video_path = config.get("video_path")

# setup path
if use_camera:
    cap = cv2.VideoCapture(1)
    
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
    working_detect(mpPose, pose, mpDraw, cap,Pin_buzzer)
else :
    relax_detect(mpPose, pose, mpDraw, cap)

