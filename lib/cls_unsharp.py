import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow, even2odd


class UnSharp(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__proc_flag = False

        if len(param) == 5:
            self.__kernel_x = param[0]
            self.__kernel_y = param[1]
            self.__sigma = param[2]
            self.__amount = param[3]
            self.__threshold = param[4]
        else:
            self.__kernel_x = 3
            self.__kernel_y = 3
            self.__sigma = 1
            self.__amount = 1
            self.__threshold = 1

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__unsharp_fillter()

        if gui:
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = tk.Scale(self.settings_frame)
        self.__scale1.configure(from_=1, to=30,
                                label="kernel x", orient="horizontal", command=self.__onScale)
        self.__scale1.pack(side="top")

        self.__scale2 = tk.Scale(self.settings_frame)
        self.__scale2.configure(from_=1, to=30,
                                label="kernel y", orient="horizontal", command=self.__onScale)
        self.__scale2.pack(side="top")

        self.__scale3 = tk.Scale(self.settings_frame)
        self.__scale3.configure(from_=0, to=100,
                                label="sigma", orient="horizontal", command=self.__onScale)
        self.__scale3.pack(side="top")

        self.__scale4 = tk.Scale(self.settings_frame)
        self.__scale4.configure(from_=0, to=100,
                                label="amount", orient="horizontal", command=self.__onScale)
        self.__scale4.pack(side="top")

        self.__scale5 = tk.Scale(self.settings_frame)
        self.__scale5.configure(from_=0, to=100,
                                label="threshold", orient="horizontal", command=self.__onScale)
        self.__scale5.pack(side="top")

        self.__scale1.set(self.__kernel_x)
        self.__scale2.set(self.__kernel_y)
        self.__scale3.set(self.__sigma)
        self.__scale4.set(self.__amount)
        self.__scale5.set(self.__threshold)
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
        self.__sigma = self.__scale3.get()
        self.__amount = self.__scale4.get()
        self.__threshold = self.__scale5.get()
        self.dst_img = self.__unsharp_fillter()
        self.Draw()
        self.__proc_flag = False
        pass

    def __unsharp_fillter(self):
        img_copy = self.origin_img.copy()

        self.__kernel_x = even2odd(self.__kernel_x)
        self.__kernel_y = even2odd(self.__kernel_y)

        blurred = cv2.GaussianBlur(img_copy,
                                   (self.__kernel_x, self.__kernel_y),
                                   self.__sigma)
        sharpened = float(self.__amount + 1) * img_copy - \
            float(self.__amount) * blurred
        sharpened = np.maximum(sharpened, np.zeros(sharpened.shape))
        sharpened = np.minimum(sharpened, 255 * np.ones(sharpened.shape))
        sharpened = sharpened.round().astype(np.uint8)
        if self.__threshold > 0:
            low_contrast_mask = np.absolute(
                img_copy - blurred) < self.__threshold
            np.copyto(sharpened, img_copy, where=low_contrast_mask)

        return sharpened

    def get_data(self):
        param = []
        param.append(self.__kernel_x)
        param.append(self.__kernel_y)
        param.append(self.__sigma)
        param.append(self.__amount)
        param.append(self.__threshold)
        print('Proc : UnSharp')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    param = [5, 5, 0, 12, 25]
    app = UnSharp(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./UnSharp.jpg', dst_img)
