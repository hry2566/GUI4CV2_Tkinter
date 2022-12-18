import tkinter as tk

import cv2

from lib.gui.cls_edit_window import EditWindow, even2odd
from lib.parts.parts_scale import Parts_Scale


class Gaussian_Blur(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__kernel_x = 1
        self.__kernel_y = 1
        self.__std = 1
        self.__proc_flag = False
        self.__gui = gui

        if len(param) == 3:
            self.__kernel_x = param[0]
            self.__kernel_y = param[1]
            self.__std = param[2]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__gaussian_blur()

        if gui:
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = Parts_Scale(self.settings_frame)
        self.__scale1.configure(label='kernel_x', side='top', from_=1, to=50)
        self.__scale2 = Parts_Scale(self.settings_frame)
        self.__scale2.configure(label='kernel', side='top', from_=1, to=50)
        self.__scale3 = Parts_Scale(self.settings_frame)
        self.__scale3.configure(label='std', side='top', from_=1, to=50)

        self.__scale1.set(self.__kernel_x)
        self.__scale2.set(self.__kernel_y)
        self.__scale3.set(self.__std)

    def __init_events(self):
        self.__scale1.bind(changed=self.__onScale)
        self.__scale2.bind(changed=self.__onScale)
        self.__scale3.bind(changed=self.__onScale)

    def __onScale(self):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__kernel_x = self.__scale1.get()
        self.__kernel_y = self.__scale2.get()
        self.__std = self.__scale3.get()
        self.dst_img = self.__gaussian_blur()
        self.Draw()
        self.__proc_flag = False
        pass

    def __gaussian_blur(self):
        img_copy = self.origin_img.copy()
        self.__kernel_x = even2odd(self.__kernel_x)
        self.__kernel_y = even2odd(self.__kernel_y)

        img = cv2.GaussianBlur(img_copy,
                               (self.__kernel_x, self.__kernel_y),
                               self.__std)
        return img

    def get_data(self):
        param = []
        param.append(self.__kernel_x)
        param.append(self.__kernel_y)
        param.append(self.__std)
        if self.__gui:
            print('Proc : Gaussian Blur')
            print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    param = [33, 33, 3]
    app = Gaussian_Blur(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./Gaussian_Blur.jpg', dst_img)
