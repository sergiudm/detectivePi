import cv2
import mediapipe as mp
import time
from .common import is_sitting, is_slouching

# import RPi.GPIO as GPIO
# import smbus

def relax_detect(mpPose, pose, mpDraw, cap, vis=True):
    pass