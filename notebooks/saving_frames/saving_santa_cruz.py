import os
import sys
import cv2
import numpy as np
import pandas as pd
from PIL import Image

sys.path.append('../../codes')
from utils import video_utils

ALL_FRAMES_STRING = 'santa-cruz/frames/all/'
OVERLAPED = '../../Regioes/santa-cruz/dataFrames/overlaped/'

VIDEO_PATH = '../../Dataset/videos/santa-cruz/'
VIDEO_NAMES = ['20210225_rectified_DJI_0067.avi','20210225_rectified_DJI_0068.avi']

video_capture = []
video_capture.append(cv2.VideoCapture(VIDEO_PATH+VIDEO_NAMES[0]))
video_capture.append(cv2.VideoCapture(VIDEO_PATH+VIDEO_NAMES[1]))

