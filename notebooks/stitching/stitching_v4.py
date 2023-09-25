import os
import sys
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

sys.path.append('../../codes')
from utils import video_utils

TUBIACANGA  = '../../Regioes/tubiacanga/'
PACIENCIA   = '../../Regioes/paciencia/'
SEPETIBA    = '../../Regioes/sepetiba/'
SANTA_CRUZ  = '../../Regioes/santa-cruz/'

STRING_BODY = 'frame_{}.jpeg'
IMAGE_PATH = 'frames/'
DATA_FRAME_PATH = 'dataFrames/'

def cumulative_sum2 (data_frame_path, image_path, translation = 0.2):
  df = pd.read_csv(data_frame_path)
  x = df['x']
  y = df['y']

  frame = np.array(Image.open(image_path + '/frame_0001.jpeg'))
  
  y_diff = int(frame.shape[0] - frame.shape[0]*translation)
  x_diff = int(frame.shape[1] - frame.shape[1]*translation)

  frames_desloc = []
  counter = 0
  aux = [0,0]
  for i in range(x.shape[0]):
    while (aux[0] < x_diff) or (aux[1] < y_diff):
      counter += 1
      aux[0] += x[counter]
      aux[1] += y[counter]
      if (abs(df['y'][counter]) > abs(df['x'][counter])):
        aux += abs(df['y'][counter])
    frames_desloc.append([(x,y),counter])
  return frames_desloc

results = cumulative_sum2(SANTA_CRUZ+'dataFrames/all/phase_correlate.csv', SANTA_CRUZ+)
print (results)