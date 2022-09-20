
import cv2
from lib.cls_average import Average

img = cv2.imread('./0000_img/opencv_logo.jpg')
param = []
average = Average(img, param, gui=True)
param, dst_img = average.get_data()
