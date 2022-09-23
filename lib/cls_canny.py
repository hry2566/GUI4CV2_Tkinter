import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow, even2odd


class Canny(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__proc_flag = False

        if len(param) == 3:
            self.kernel = param[0]
            self.max_val = param[1]
            self.min_val = param[2]
            mode = 1
        else:
            self.kernel = 0
            self.max_val = 0
            self.min_val = 0
            mode = 0

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__canny(mode)

        if gui:
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.scale1 = tk.Scale(self.settings_frame)
        self.scale1.configure(from_=1, to=50,
                              label="kernel", orient="horizontal", command=self.__onScale)
        self.scale1.pack(side="top")
        self.scale2 = tk.Scale(self.settings_frame)
        self.scale2.configure(from_=0, to=500,
                              label="max_val", orient="horizontal", command=self.__onScale)
        self.scale2.pack(side="top")
        self.scale3 = tk.Scale(self.settings_frame)
        self.scale3.configure(from_=0, to=500,
                              label="min_val", orient="horizontal", command=self.__onScale)
        self.scale3.pack(side="top")

        self.scale1.set(self.kernel)
        self.scale2.set(self.max_val)
        self.scale3.set(self.min_val)
        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.kernel = self.scale1.get()
        self.max_val = self.scale2.get()
        self.min_val = self.scale3.get()

        mode = 1
        self.dst_img = self.__canny(mode)
        self.Draw()
        self.__proc_flag = False
        pass

    def __canny(self, mode: int):
        img_copy = self.origin_img.copy()
        img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

        if mode == 0:
            med_val = np.median(img_gray)
            sigma = 0.33  # 0.33
            self.min_val = int(max(0, (1.0 - sigma) * med_val))
            self.max_val = int(max(255, (1.0 + sigma) * med_val))

            self.scale1.set(self.kernel)
            self.scale2.set(self.max_val)
            self.scale3.set(self.min_val)

        # if self.kernel % 2 == 0:
        #     self.kernel += 1

        self.kernel = even2odd(self.kernel)

        # ぼかし
        img_blur = cv2.GaussianBlur(img_gray, (self.kernel, self.kernel), None)

        # 輪郭抽出
        img = cv2.Canny(img_blur,
                        threshold1=self.max_val,
                        threshold2=self.min_val)

        return img

    def get_data(self):
        param = []
        param.append(self.kernel)
        param.append(self.max_val)
        param.append(self.min_val)
        print('Proc : Canny')
        print(f'param = {param}')
        img = cv2.cvtColor(self.dst_img, cv2.COLOR_GRAY2BGR)
        return param, img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    param = [5, 6, 18]
    app = Canny(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./canny.jpg', dst_img)
