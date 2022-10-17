import tkinter as tk

import cv2

from lib.gui.cls_edit_window import EditWindow


class ConvertScaleAbs(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__alpha = 1
        self.__beta = 0
        self.__proc_flag = False

        if len(param) == 2:
            self.__alpha = param[0]
            self.__beta = param[1]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()
            self.run()
        else:
            self.dst_img = self.__convert_scale_abs()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = tk.Scale(self.settings_frame)
        self.__scale1.configure(from_=1, to=3,
                                label="contrast", orient="horizontal", resolution=0.01, command=self.__onScale)
        self.__scale1.pack(side="top")

        self.__scale2 = tk.Scale(self.settings_frame)
        self.__scale2.configure(from_=-128, to=128,
                                label="brightness", orient="horizontal", command=self.__onScale)
        self.__scale2.pack(side="top")

        self.__scale1.set(self.__alpha)
        self.__scale2.set(self.__beta)
        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__alpha = self.__scale1.get()
        self.__beta = self.__scale2.get()
        self.dst_img = self.__convert_scale_abs()
        self.Draw()
        self.__proc_flag = False
        pass

    def __convert_scale_abs(self):
        img = cv2.convertScaleAbs(
            self.origin_img, alpha=self.__alpha, beta=self.__beta)
        return img

    def get_data(self):
        param = []
        param.append(self.__alpha)
        param.append(self.__beta)
        print('Proc : ConvertScaleAbs')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    param = [2.12, -34]
    app = ConvertScaleAbs(img, param, gui=False)
    param, dst_img = app.get_data()
    cv2.imwrite('./ConvertScaleAbs.jpg', dst_img)
