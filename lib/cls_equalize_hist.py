"""平坦化"""
import tkinter as tk

import cv2

from lib.gui.cls_edit_window import EditWindow
from lib.parts.parts_scale import Parts_Scale


class EqualizeHist(EditWindow):
    """平坦化クラス"""

    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__h_flag = True
        self.__s_flag = True
        self.__v_flag = True
        self.clip_limit = 1.0
        self.gridsize = 1
        self.__proc_flag = False
        self.__gui = gui

        if len(param) == 5:
            self.__h_flag = param[0]
            self.__s_flag = param[1]
            self.__v_flag = param[2]
            self.clip_limit = param[3]
            self.gridsize = param[4]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__equalize_hist()

        if gui:
            self.draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__h_bool = tk.BooleanVar()
        self.__s_bool = tk.BooleanVar()
        self.__v_bool = tk.BooleanVar()

        self.__h_bool.set(self.__h_flag)
        self.__s_bool.set(self.__s_flag)
        self.__v_bool.set(self.__v_flag)

        self.checkbutton1 = tk.Checkbutton(
            self.settings_frame, variable=self.__h_bool, command=self.__on_click)
        self.checkbutton1.configure(text="Hue",)
        self.checkbutton1.pack(side="top", anchor='w')
        self.checkbutton2 = tk.Checkbutton(
            self.settings_frame, variable=self.__s_bool, command=self.__on_click)
        self.checkbutton2.configure(text="Saturation")
        self.checkbutton2.pack(side="top", anchor='w')
        self.checkbutton3 = tk.Checkbutton(
            self.settings_frame, variable=self.__v_bool, command=self.__on_click)
        self.checkbutton3.configure(text="Value")
        self.checkbutton3.pack(side="top", anchor='w')

        self.__scale1 = Parts_Scale(self.settings_frame)
        self.__scale1.configure(
            label='clip_limit', side='top', resolution=0.1, from_=1, to=10)
        self.__scale2 = Parts_Scale(self.settings_frame)
        self.__scale2.configure(
            label='grid_size', side='top', from_=1, to=100)

        self.__scale1.set(self.clip_limit)
        self.__scale2.set(self.gridsize)

    def __init_events(self):
        self.__scale1.bind(changed=self.__on_scale)
        self.__scale2.bind(changed=self.__on_scale)

    def __on_click(self):
        self.__h_flag = self.__h_bool.get()
        self.__s_flag = self.__s_bool.get()
        self.__v_flag = self.__v_bool.get()

        self.dst_img = self.__equalize_hist()
        self.draw()

    def __on_scale(self):
        if self.__proc_flag:
            return
        self.__proc_flag = True
        self.clip_limit = self.__scale1.get()
        self.gridsize = self.__scale2.get()
        self.dst_img = self.__equalize_hist()
        self.draw()
        self.__proc_flag = False

    def __equalize_hist(self):
        img_copy = self.origin_img.copy()

        h_1, s_1, v_1 = cv2.split(cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV))
        clahe = cv2.createCLAHE(clipLimit=self.clip_limit,
                                tileGridSize=(self.gridsize, self.gridsize))
        if self.__h_flag:
            h_1 = clahe.apply(h_1)
        if self.__s_flag:
            s_1 = clahe.apply(s_1)
        if self.__v_flag:
            v_1 = clahe.apply(v_1)
        img = cv2.cvtColor(cv2.merge((h_1, s_1, v_1)), cv2.COLOR_HSV2BGR)
        return img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.__h_flag)
        param.append(self.__s_flag)
        param.append(self.__v_flag)
        param.append(self.clip_limit)
        param.append(self.gridsize)
        if self.__gui:
            print('Proc : EqualizeHist')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     img = cv2.imread('./0000_img/I.jpg')
#     # param = []
#     param = [False, False, True, 2.3, 17]
#     app = EqualizeHist(img, param, gui=True)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./EqualizeHist.jpg', dst_img)
