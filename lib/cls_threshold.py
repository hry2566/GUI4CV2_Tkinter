import tkinter as tk

import cv2

from lib.gui.cls_edit_window import EditWindow


class Threshold(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__thresh = 1
        self.__val = 255
        self.__proc_flag = False

        if len(param) == 2:
            self.__thresh = param[0]
            self.__val = param[1]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()
            self.run()
        else:
            self.dst_img = self.__threshold()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = tk.Scale(self.settings_frame)
        self.__scale1.configure(from_=1, to=255,
                                label="thresh", orient="horizontal", command=self.__onScale)
        self.__scale1.pack(side="top")

        self.__scale2 = tk.Scale(self.settings_frame)
        self.__scale2.configure(from_=1, to=255,
                                label="val", orient="horizontal", command=self.__onScale)
        self.__scale2.pack(side="top")

        self.__scale1.set(self.__thresh)
        self.__scale2.set(self.__val)
        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__thresh = self.__scale1.get()
        self.__val = self.__scale2.get()
        self.dst_img = self.__threshold()
        self.Draw()
        self.__proc_flag = False
        pass

    def __threshold(self):
        img_copy = self.origin_img.copy()
        img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

        _, img = cv2.threshold(
            img_gray, self.__thresh, self.__val, cv2.THRESH_BINARY_INV)

        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img

    def get_data(self):
        param = []
        param.append(self.__thresh)
        param.append(self.__val)
        print('Proc : Threshold')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    param = [23, 255]
    app = Threshold(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./Threshold.jpg', dst_img)
