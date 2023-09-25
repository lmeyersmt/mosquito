# import os
# import sys
import cv2
import numpy as np
import pandas as pd
# import matplotlib.pyplot as plt
# from PIL import Image

# sys.path.append('../../codes')
# from utils import video_utils

TUBIACANGA  = '../../Regioes/tubiacanga/'
PACIENCIA   = '../../Regioes/paciencia/'
SEPETIBA    = '../../Regioes/sepetiba/'
SANTA_CRUZ  = '../../Regioes/santa-cruz/'

STRING_BODY = 'frame_{}.jpeg'
IMAGE_PATH = 'frames/'
DATA_FRAME_PATH = 'dataFrames/'

def cumulative_sum2 (data_frame_path, video_path, translation = 0.2):
  df = pd.read_csv(data_frame_path)
  x = df['x']
  y = df['y']

  video = cv2.VideoCapture(video_path)
  frame = video.read()[1]
  
  y_diff = int(frame.shape[0] - frame.shape[0]*translation)
  x_diff = int(frame.shape[1] - frame.shape[1]*translation)

  frames_desloc = []
  counter = 0
  while counter < df.shape[0]:
    aux = [0,0]
    while (aux[0] < x_diff) or (aux[1] < y_diff):
      if counter < df.shape[0]:
        aux[0] += x[counter]
        aux[1] += y[counter]
        counter+=1
      else:
        exit
    frames_desloc.append([(aux[0],aux[1]),counter])
  return frames_desloc

df_overlaped = cumulative_sum2('../../Regioes/santa-cruz/dataFrames/all/phase_correlate.csv', '../../Dataset/videos/santa-cruz/20210225_rectified_DJI_0067.avi')
df_overlaped.to_csv('../../Regioes/santa-cruz/dataFrames/overlaped/phase_correlate02.csv')