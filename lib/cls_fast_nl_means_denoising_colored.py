import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class FastNlMeansDenoisingColored(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__h = 3
        self.__hColor = 20
        self.__templateWindowSize = 5
        self.__searchWindowSize = 20
        self.__proc_flag = False

        if len(param) == 4:
            self.__h = param[0]
            self.__hColor = param[1]
            self.__templateWindowSize = param[2]
            self.__searchWindowSize = param[3]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()
            self.run()
        else:
            self.dst_img = self.__fast_nl_means_denoising_colored()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = tk.Scale(self.settings_frame)
        self.__scale1.configure(from_=0, to=20,
                                label="h", orient="horizontal", command=self.__onScale)
        self.__scale1.pack(side="top")

        self.__scale2 = tk.Scale(self.settings_frame)
        self.__scale2.configure(from_=0, to=20,
                                label="hColor", orient="horizontal", command=self.__onScale)
        self.__scale2.pack(side="top")

        self.__scale3 = tk.Scale(self.settings_frame)
        self.__scale3.configure(from_=0, to=10,
                                label="templateWindowSize", orient="horizontal", command=self.__onScale)
        self.__scale3.pack(side="top")

        self.__scale4 = tk.Scale(self.settings_frame)
        self.__scale4.configure(from_=0, to=30,
                                label="searchWindowSize", orient="horizontal", command=self.__onScale)
        self.__scale4.pack(side="top")

        self.__scale1.set(self.__h)
        self.__scale2.set(self.__hColor)
        self.__scale3.set(self.__templateWindowSize)
        self.__scale4.set(self.__searchWindowSize)
        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__h = self.__scale1.get()
        self.__hColor = self.__scale2.get()
        self.__templateWindowSize = self.__scale3.get()
        self.__searchWindowSize = self.__scale4.get()
        self.dst_img = self.__fast_nl_means_denoising_colored()
        self.Draw()
        self.__proc_flag = False
        pass

    def __fast_nl_means_denoising_colored(self):
        img = cv2.fastNlMeansDenoisingColored(
            self.origin_img,
            None,
            self.__h,
            self.__hColor,
            self.__templateWindowSize,
            self.__searchWindowSize)
        return img

    def get_data(self):
        param = []
        param.append(self.__h)
        param.append(self.__hColor)
        param.append(self.__templateWindowSize)
        param.append(self.__searchWindowSize)
        print('Proc : FastNlMeansDenoisingColored')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/I.jpg')
    param = []
    param = [10, 20, 5, 20]
    app = FastNlMeansDenoisingColored(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./FastNlMeansDenoisingColored.jpg', dst_img)
