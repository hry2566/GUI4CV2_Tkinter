import tkinter as tk

import cv2

from lib.gui.cls_edit_window import EditWindow


class Bilateral_Filter(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__proc_flag = False

        if len(param) == 3:
            self.d = param[0]
            self.sigma_color = param[1]
            self.sigma_space = param[2]
        else:
            self.d = 0
            self.sigma_color = 0
            self.sigma_space = 0

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__bilateral_filter()

        if gui:
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.scale1 = tk.Scale(self.settings_frame)
        self.scale1.configure(from_=-128, to=128,
                              label="d", orient="horizontal", command=self.__onScale)
        self.scale1.pack(side="top")
        self.scale2 = tk.Scale(self.settings_frame)
        self.scale2.configure(from_=0, to=30,
                              label="sigma_color", orient="horizontal", command=self.__onScale)
        self.scale2.pack(side="top")
        self.scale3 = tk.Scale(self.settings_frame)
        self.scale3.configure(from_=0, to=30,
                              label="sigma_space", orient="horizontal", command=self.__onScale)
        self.scale3.pack(side="top")

        self.scale1.set(self.d)
        self.scale2.set(self.sigma_color)
        self.scale3.set(self.sigma_space)
        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.d = self.scale1.get()
        self.sigma_color = self.scale2.get()
        self.sigma_space = self.scale3.get()

        self.dst_img = self.__bilateral_filter()
        self.Draw()
        self.__proc_flag = False
        pass

    def __bilateral_filter(self):
        img_copy = self.origin_img.copy()

        img = cv2.bilateralFilter(img_copy,
                                  d=self.d,
                                  sigmaColor=self.sigma_color,
                                  sigmaSpace=self.sigma_space)
        return img

    def get_data(self):
        param = []
        param.append(self.d)
        param.append(self.sigma_color)
        param.append(self.sigma_space)
        print('Proc : Bilateral_Filter')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    param = [60, 30, 30]
    app = Bilateral_Filter(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./bilateral_filter.jpg', dst_img)
