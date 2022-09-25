import cv2
from lib.cls_average import Average

img = cv2.imread('./0000_img/opencv_logo.jpg')

param = [15, 15]
average = Average(img, param, gui=False)
param, dst_img = average.get_data()

cv2.imwrite('test.jpg', dst_img)
