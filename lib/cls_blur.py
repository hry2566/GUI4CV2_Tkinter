import tkinter as tk

import cv2

from lib.gui.cls_edit_window import EditWindow


class Blur(EditWindow):
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

        self.dst_img = self.__blur()

        if gui:
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale_x = tk.Scale(self.settings_frame)
        self.__scale_x.configure(from_=1, to=50,
                                 label="kernel x", orient="horizontal", command=self.__onScale)
        self.__scale_x.pack(side="top")

        self.__scale_y = tk.Scale(self.settings_frame)
        self.__scale_y.configure(from_=1, to=50,
                                 label="kernel y", orient="horizontal", command=self.__onScale)
        self.__scale_y.pack(side="top")

        self.__scale_x.set(self.__kernel_x)
        self.__scale_y.set(self.__kernel_y)
        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__kernel_x = self.__scale_x.get()
        self.__kernel_y = self.__scale_y.get()
        self.dst_img = self.__blur()
        self.Draw()
        self.__proc_flag = False
        pass

    def __blur(self):
        img_copy = self.origin_img.copy()
        img = cv2.blur(img_copy, (self.__kernel_x, self.__kernel_y))
        return img

    def get_data(self):
        param = []
        param.append(self.__kernel_x)
        param.append(self.__kernel_y)
        print('Proc : Blur')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    param = [15, 15]
    app = Blur(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./blur.jpg', dst_img)
