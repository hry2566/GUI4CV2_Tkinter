"""二値化(InRange)"""
import tkinter as tk
import numpy as np
import cv2

from lib.gui.cls_edit_window import EditWindow
from lib.parts.parts_scale import Parts_Scale


class InRange(EditWindow):
    """二値化(InRange)クラス"""

    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__proc_flag = False
        self.__p1min = 0
        self.__p1max = 255
        self.__p2min = 0
        self.__p2max = 255
        self.__p3min = 0
        self.__p3max = 255
        self.__flag = False
        self.__gui = gui

        if len(param) == 7:
            self.__p1min = param[0]
            self.__p1max = param[1]
            self.__p2min = param[2]
            self.__p2max = param[3]
            self.__p3min = param[4]
            self.__p3max = param[5]
            self.__flag = param[6]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__inrange()

        if gui:
            self.draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.var = tk.IntVar()

        self.option_frame = tk.Frame(self.settings_frame)
        self.option_frame.configure(height=200, width=200)
        self.radiobutton1 = tk.Radiobutton(
            self.option_frame, value=0, variable=self.var)
        self.radiobutton1.configure(text='RGB')
        self.radiobutton1.pack(expand="true", fill="x", side="left")
        self.radiobutton2 = tk.Radiobutton(
            self.option_frame, value=1, variable=self.var)
        self.radiobutton2.configure(text='HSV')
        self.radiobutton2.pack(expand="true", fill="x", side="left")
        self.option_frame.pack(fill="x", side="top")
        self.rgb_frame = tk.LabelFrame(self.settings_frame)
        self.rgb_frame.configure(height=200, text='RGB', width=200)
        self.scale_rmin = Parts_Scale(self.rgb_frame)
        self.scale_rmin.configure(label='R_min', side='top', from_=0, to=255)
        self.scale_rmax = Parts_Scale(self.rgb_frame)
        self.scale_rmax.configure(label='R_max', side='top', from_=0, to=255)
        self.scale_gmin = Parts_Scale(self.rgb_frame)
        self.scale_gmin.configure(label='G_min', side='top', from_=0, to=255)
        self.scale_gmax = Parts_Scale(self.rgb_frame)
        self.scale_gmax.configure(label='G_max', side='top', from_=0, to=255)
        self.scale_bmin = Parts_Scale(self.rgb_frame)
        self.scale_bmin.configure(label='B_min', side='top', from_=0, to=255)
        self.scale_bmax = Parts_Scale(self.rgb_frame)
        self.scale_bmax.configure(label='B_max', side='top', from_=0, to=255)
        self.rgb_frame.pack(fill="x", side="top")
        self.hsv_frame = tk.LabelFrame(self.settings_frame)
        self.hsv_frame.configure(height=200, text='HSV', width=200)
        self.scale_hmin = Parts_Scale(self.hsv_frame)
        self.scale_hmin.configure(label='H_min', side='top', from_=0, to=255)
        self.scale_hmax = Parts_Scale(self.hsv_frame)
        self.scale_hmax.configure(label='H_max', side='top', from_=0, to=255)
        self.scale_smin = Parts_Scale(self.hsv_frame)
        self.scale_smin.configure(label='S_min', side='top', from_=0, to=255)
        self.scale_smax = Parts_Scale(self.hsv_frame)
        self.scale_smax.configure(label='S_max', side='top', from_=0, to=255)
        self.scale_vmin = Parts_Scale(self.hsv_frame)
        self.scale_vmin.configure(label='V_min', side='top', from_=0, to=255)
        self.scale_vmax = Parts_Scale(self.hsv_frame)
        self.scale_vmax.configure(label='V_max', side='top', from_=0, to=255)
        self.hsv_frame.pack(side="top")

        if not self.__flag:
            self.__show_mode(0)
            self.var.set(0)
            self.scale_rmin.set(self.__p1min)
            self.scale_rmax.set(self.__p1max)
            self.scale_gmin.set(self.__p2min)
            self.scale_gmax.set(self.__p2max)
            self.scale_bmin.set(self.__p3min)
            self.scale_bmax.set(self.__p3max)
            self.scale_hmax.set(255)
            self.scale_smax.set(255)
            self.scale_vmax.set(255)
        else:
            self.__show_mode(1)
            self.var.set(1)
            self.scale_hmin.set(self.__p1min)
            self.scale_hmax.set(self.__p1max)
            self.scale_smin.set(self.__p2min)
            self.scale_smax.set(self.__p2max)
            self.scale_vmin.set(self.__p3min)
            self.scale_vmax.set(self.__p3max)
            self.scale_rmax.set(255)
            self.scale_gmax.set(255)
            self.scale_bmax.set(255)

    def __init_events(self):
        self.radiobutton1.configure(command=self.__on_click_optbtn)
        self.radiobutton2.configure(command=self.__on_click_optbtn)
        self.scale_rmin.bind(changed=self.__on_scale)
        self.scale_rmax.bind(changed=self.__on_scale)
        self.scale_gmin.bind(changed=self.__on_scale)
        self.scale_gmax.bind(changed=self.__on_scale)
        self.scale_bmin.bind(changed=self.__on_scale)
        self.scale_bmax.bind(changed=self.__on_scale)

        self.scale_hmin.bind(changed=self.__on_scale)
        self.scale_hmax.bind(changed=self.__on_scale)
        self.scale_smin.bind(changed=self.__on_scale)
        self.scale_smax.bind(changed=self.__on_scale)
        self.scale_vmin.bind(changed=self.__on_scale)
        self.scale_vmax.bind(changed=self.__on_scale)

    def __on_click_optbtn(self):
        mode = self.var.get()
        if mode == 0:
            self.__flag = False
        self.__flag = True
        self.__show_mode(mode)
        self.__get_param_val(mode)
        self.dst_img = self.__inrange()
        self.draw()

    def __get_param_val(self, mode):
        if mode == 0:
            self.__p1min = self.scale_rmin.get()
            self.__p1max = self.scale_rmax.get()
            self.__p2min = self.scale_gmin.get()
            self.__p2max = self.scale_gmax.get()
            self.__p3min = self.scale_bmin.get()
            self.__p3max = self.scale_bmax.get()
        else:
            self.__p1min = self.scale_hmin.get()
            self.__p1max = self.scale_hmax.get()
            self.__p2min = self.scale_smin.get()
            self.__p2max = self.scale_smax.get()
            self.__p3min = self.scale_vmin.get()
            self.__p3max = self.scale_vmax.get()

    def __on_scale(self):
        if self.__proc_flag:
            return
        self.__proc_flag = True
        self.__get_param_val(self.var.get())
        self.dst_img = self.__inrange()
        self.draw()
        self.__proc_flag = False

    def __show_mode(self, mode):
        if mode == 0:
            self.hsv_frame.pack_forget()
            self.rgb_frame.pack()
        else:
            self.rgb_frame.pack_forget()
            self.hsv_frame.pack()

    def __inrange(self):
        img_copy = self.origin_img.copy()

        if not self.__flag:
            img_copy = cv2.inRange(img_copy,
                                   (self.__p3min, self.__p2min, self.__p1min),
                                   (self.__p3max, self.__p2max, self.__p1max))
        else:
            img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV_FULL)
            h_low = self.__p1min
            h_high = self.__p1max
            s_low = self.__p2min
            s_high = self.__p2max
            v_low = self.__p3min
            v_high = self.__p3max

            if h_low > h_high:
                lower_color1 = np.array([h_low, s_low, v_low])
                upper_color1 = np.array([255, s_high, v_high])
                # 指定した範囲内を白、それ以外を黒にする（マスク画像の生成
                mask1 = cv2.inRange(img_copy, lower_color1, upper_color1)
                # 取得する色の範囲を指定する
                lower_color2 = np.array([0, s_low, v_low])
                upper_color2 = np.array([h_high, s_high, v_high])
                # 指定した範囲内を白、それ以外を黒にする（マスク画像の生成
                mask2 = cv2.inRange(img_copy, lower_color2, upper_color2)
                # マスクの結合
                img_copy = mask1 + mask2
            else:
                # 取得する色の範囲を指定する
                lower_color = np.array([h_low, s_low, v_low])
                upper_color = np.array([h_high, s_high, v_high])
                # 指定した範囲内を白、それ以外を黒にする（マスク画像の生成
                img_copy = cv2.inRange(img_copy, lower_color, upper_color)
        return img_copy

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.__p1min)
        param.append(self.__p1max)
        param.append(self.__p2min)
        param.append(self.__p2max)
        param.append(self.__p3min)
        param.append(self.__p3max)
        param.append(self.__flag)

        img = self.dst_img
        if len(self.dst_img.shape) == 2:
            img = cv2.cvtColor(self.dst_img, cv2.COLOR_GRAY2BGR)
        if self.__gui:
            print('Proc : inRange')
            print(f'param = {param}')
        return param, img


# if __name__ == "__main__":
#     # img = cv2.imread('./0000_img/I.jpg')
#     img = cv2.imread('./0000_img/opencv_logo.jpg')
#     param = []
#     # param = [0, 161, 184, 255, 0, 255, False]   # RGB
#     # param = [191, 49, 191, 255, 191, 255, True]  # HSV
#     app = InRange(img, param, gui=True)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./inrange.jpg', dst_img)
