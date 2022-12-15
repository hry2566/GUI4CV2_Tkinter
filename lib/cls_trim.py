import tkinter as tk

import cv2

from lib.gui.cls_edit_window import EditWindow
from lib.parts.parts_scale import Parts_Scale


class Trim(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__x1 = 0
        self.__y1 = 0
        self.__x2 = self.origin_img.shape[1]
        self.__y2 = self.origin_img.shape[0]
        self.__proc_flag = False

        if len(param) == 4:
            self.__x1 = param[0]
            self.__y1 = param[1]
            self.__x2 = param[2]
            self.__y2 = param[3]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__trim()

        if gui:
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.scale_x1 = Parts_Scale(self.settings_frame)
        self.scale_x1.configure(label='x1', side='top',
                                from_=0, to=self.origin_img.shape[1])
        self.scale_y1 = Parts_Scale(self.settings_frame)
        self.scale_y1.configure(label='y1', side='top',
                                from_=0, to=self.origin_img.shape[0])
        self.scale_x2 = Parts_Scale(self.settings_frame)
        self.scale_x2.configure(label='x2', side='top',
                                from_=0, to=self.origin_img.shape[1])
        self.scale_y2 = Parts_Scale(self.settings_frame)
        self.scale_y2.configure(label='y2', side='top',
                                from_=0, to=self.origin_img.shape[0])

        self.scale_x1.set(self.__x1)
        self.scale_y1.set(self.__y1)
        self.scale_x2.set(self.__x2)
        self.scale_y2.set(self.__y2)
        pass

    def __init_events(self):
        self.scale_x1.bind(changed=self.__onScale)
        self.scale_y1.bind(changed=self.__onScale)
        self.scale_x2.bind(changed=self.__onScale)
        self.scale_y2.bind(changed=self.__onScale)
        pass

    def __onScale(self):
        if self.__proc_flag:
            return
        self.__proc_flag = True
        self.__x1 = self.scale_x1.get()
        self.__y1 = self.scale_y1.get()
        self.__x2 = self.scale_x2.get()
        self.__y2 = self.scale_y2.get()

        self.scale_x2.configure(from_=self.__x1+1)
        self.scale_y2.configure(from_=self.__y1+1)
        self.scale_x1.configure(to=self.__x2-1)
        self.scale_y1.configure(to=self.__y2-1)

        self.dst_img = self.__trim()
        self.Draw()
        self.__proc_flag = False
        pass

    def __trim(self):
        img_copy = self.origin_img.copy()
        if (self.__x1 < self.__x2) and (self.__y1 < self.__y2):
            img_copy = img_copy[self.__y1: self.__y2, self.__x1: self.__x2]
        return img_copy

    def get_data(self):
        param = []
        param.append(self.__x1)
        param.append(self.__y1)
        param.append(self.__x2)
        param.append(self.__y2)
        print('Proc : Trim')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    # img = cv2.imread('./0000_img/ECU/ECUlow_1.jpg')
    param = []
    # param = [6, 115, 113, 227]
    app = Trim(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./Trim.jpg', dst_img)
