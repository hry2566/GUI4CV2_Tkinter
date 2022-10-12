import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class Shading_MovingAve(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__kernel_x = 1
        self.__kernel_y = 1
        self.__noise_cut = 0
        self.__proc_flag = False

        if len(param) == 3:
            self.__kernel_x = param[0]
            self.__kernel_y = param[1]
            self.__noise_cut = param[2]
        else:
            self.__kernel_x = 1
            self.__kernel_y = 1
            self.__noise_cut = 0

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__shading_moving_ave()

        if gui:
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = tk.Scale(self.settings_frame)
        self.__scale1.configure(from_=1, to=100,
                                label='kernel x', orient='horizontal', command=self.__onScale)
        self.__scale1.pack(side='top')

        self.__scale2 = tk.Scale(self.settings_frame)
        self.__scale2.configure(from_=1, to=100,
                                label='kernel y', orient='horizontal', command=self.__onScale)
        self.__scale2.pack(side='top')

        self.__scale3 = tk.Scale(self.settings_frame)
        self.__scale3.configure(from_=0, to=255,
                                label='remove noise', orient='horizontal', command=self.__onScale)
        self.__scale3.pack(side='top')

        self.__scale1.set(self.__kernel_x)
        self.__scale2.set(self.__kernel_y)
        self.__scale3.set(self.__noise_cut)

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
        self.__noise_cut = self.__scale3.get()
        self.dst_img = self.__shading_moving_ave()
        self.Draw()
        self.__proc_flag = False

    def __shading_moving_ave(self):
        img_copy = self.origin_img.copy()
        image = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        height, width = image.shape[:2]

        num_x = self.__kernel_x  # 移動平均の個数
        kernel_x = np.ones(num_x)/num_x
        num_y = self.__kernel_y  # 移動平均の個数
        kernel_y = np.ones(num_y)/num_y

        if num_x > 1:
            for index in range(height):
                y1 = image[index:index+1, 0:width][0]
                y2 = np.convolve(y1, kernel_x, mode='same')
                dev = y1-y2
                if not self.__noise_cut == 255 and not self.__noise_cut == 0:
                    dev = np.where(abs(dev) < self.__noise_cut, 0, int(255/2))
                image[index:index+1, 0:width][0] = dev+int(255/2)

        if num_y > 1:
            for index in range(width):
                y1 = image[0:height, index:index+1].T[0]
                y2 = np.convolve(y1, kernel_y, mode='same')
                dev = y1-y2
                if not self.__noise_cut == 255 and not self.__noise_cut == 0:
                    dev = np.where(abs(dev) < self.__noise_cut, 0, int(255/2))
                image[0:height, index:index+1].T[0] = dev+int(255/2)

        img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)

        return img

    def get_data(self):
        param = []
        param.append(self.__kernel_x)
        param.append(self.__kernel_y)
        param.append(self.__noise_cut)
        print('Proc : Shading_MovingAve')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    # img = cv2.imread('./0000_img/shading.png')
    img = cv2.imread('./0000_img/I.jpg')
    param = []
    app = Shading_MovingAve(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./Shading_MovingAve.jpg', dst_img)