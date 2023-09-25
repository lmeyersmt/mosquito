import os
import sys
import cv2
import numpy as np
import pandas as pd
import time
from PIL import Image

tempo_inicial = time.time()

sys.path.append('../../codes')
from utils import video_utils

ALL_FRAMES_STRING = 'santa-cruz/frames/all/'
OVERLAPED = '../../Regioes/santa-cruz/dataFrames/overlaped/'

VIDEO_PATH = '../../Dataset/videos/santa-cruz/'
VIDEO_NAMES = ['20210225_rectified_DJI_0067.avi','20210225_rectified_DJI_0068.avi']

videos_capture = []
videos_capture.append(cv2.VideoCapture(VIDEO_PATH+VIDEO_NAMES[0]))
videos_capture.append(cv2.VideoCapture(VIDEO_PATH+VIDEO_NAMES[1]))

r_array = []
x = []
y = []
c = []
counter = 0
for i in videos_capture:
    frameB = i.read()
    while frameB[0]:
        counter += 1
        frameA = frameB
        frameB = i.read()
        if frameB[0]:
          results = video_utils.phase_correlation(frameA[1], frameB[1], 0.4)
          r_array.append(results)
          x.append(results[0][0])
          y.append(results[0][1])
          c.append(results[1])
x_dataFrame = pd.DataFrame(x)
x_dataFrame.columns = ['x']
y_dataFrame = pd.DataFrame(y)
y_dataFrame.columns = ['y']
c_dataFrame = pd.DataFrame(c)
c_dataFrame.columns = ['c']
r_dataFrame = pd.concat([x_dataFrame, y_dataFrame, c_dataFrame], axis=1)
tempo_final = time.time()
print(tempo_final - tempo_inicial, ' segundos')
# r_dataFrame.to_csv('../../Regioes/santa-cruz/dataFrames/all/phase_correlate.csv', index=False)