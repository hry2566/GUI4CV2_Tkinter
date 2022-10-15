import os
import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class CustomFillter(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__proc_flag = False

        if len(param) == 2:
            self.__kernel_x = param[0]
            self.__kernel_y = param[1]
        else:
            self.__kernel_x = 1
            self.__kernel_y = 1

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__custom_fillter()

        if gui:
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = tk.Scale(self.settings_frame)
        self.__scale1.configure(from_=1, to=50,
                                label="kernel x", orient="horizontal", command=self.__onScale)
        self.__scale1.pack(side="top")

        self.__scale2 = tk.Scale(self.settings_frame)
        self.__scale2.configure(from_=1, to=50,
                                label="kernel y", orient="horizontal", command=self.__onScale)
        self.__scale2.pack(side="top")

        self.__scale1.set(self.__kernel_x)
        self.__scale2.set(self.__kernel_y)
        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__kernel_x = self.__scale1.get()
        self.__kernel_y = self.__scale2.get()
        self.dst_img = self.__custom_fillter()
        self.Draw()
        self.__proc_flag = False
        pass

    def __custom_fillter(self):
        kernel_x = self.__kernel_x
        kernel_y = self.__kernel_y
        kernel = np.ones((kernel_y, kernel_x), np.float32)/(kernel_x*kernel_y)

        # エンボスフィルタ
        kernel = np.array([[-5, 0, 0],
                           [0, 0, 0],
                           [0, 0, 5]])

        # 微分フィルタ
        kernel = np.array([[0, 0, 0],
                           [0, -1, 1],
                           [0, 0, 0]])

        # １次微分フィルタ
        # kernel_x = np.array([[0, 0, 0],
        #                     [-1, 0, 1],
        #                     [0, 0, 0]])
        # kernel_y = np.array([[0, -1, 0],
        #                     [0, 0, 0],
        #                     [0, 1, 0]])
        # kernel_x = np.array([[-1, 0, 0],
        #                     [0, 0, 0],
        #                     [0, 0, 1]])
        # kernel_y = np.array([[0, 0, 1],
        #                     [0, 0, 0],
        #                     [-1, 0, 0]])
        kernel_x1 = np.array([[-1, -1, -1],
                              [0, 0, 0],
                              [1, 1, 1]])
        kernel_x2 = np.array([[1, 1, 1],
                              [0, 0, 0],
                              [-1, -1, -1]])
        kernel_y1 = np.array([[-1, 0, 1],
                              [-1, 0, 1],
                              [-1, 0, 1]])
        kernel_y2 = np.array([[1, 0, -1],
                              [1, 0, -1],
                              [1, 0, -1]])

        outputx1 = cv2.filter2D(
            self.origin_img, cv2.CV_64F, kernel_x1, delta=64)

        outputx2 = cv2.filter2D(
            self.origin_img, cv2.CV_64F, kernel_x2, delta=64)

        outputy1 = cv2.filter2D(
            self.origin_img, cv2.CV_64F, kernel_y1, delta=64)

        outputy2 = cv2.filter2D(
            self.origin_img, cv2.CV_64F, kernel_y2, delta=64)

        img1 = np.sqrt(outputx1 ** 2 + outputx2 ** 2)
        img2 = np.sqrt(outputy1 ** 2 + outputy2 ** 2)
        img = np.sqrt(img1 ** 2 + img2 ** 2)

        cv2.imwrite('dummy.jpg', img)
        img = cv2.imread('dummy.jpg')
        os.remove('dummy.jpg')

        # img = cv2.filter2D(self.origin_img, -1, kernel, delta=128)
        return img

    def get_data(self):
        param = []
        param.append(self.__kernel_x)
        param.append(self.__kernel_y)
        print('Proc : CustomFillter')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    # img = cv2.imread('./0000_img/opencv_logo.jpg')
    img = cv2.imread('./0000_img/2.png')
    # img = cv2.imread('./0000_img/test.jpg')
    param = []
    param = [15, 15]
    app = CustomFillter(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./average.jpg', dst_img)
