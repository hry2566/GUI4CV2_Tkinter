import tkinter as tk
import numpy as np
import cv2

from lib.gui.cls_edit_window import EditWindow
from lib.parts.parts_scale import Parts_Scale


class InRange(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        # self.__origin_bk = img
        self.__proc_flag = False
        self.__P1min = 0
        self.__P1max = 255
        self.__P2min = 0
        self.__P2max = 255
        self.__P3min = 0
        self.__P3max = 255
        self.__flag = False
        self.__gui = gui

        if len(param) == 7:
            self.__P1min = param[0]
            self.__P1max = param[1]
            self.__P2min = param[2]
            self.__P2max = param[3]
            self.__P3min = param[4]
            self.__P3max = param[5]
            self.__flag = param[6]
            pass

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__inrange()

        if gui:
            self.Draw()
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
        self.scale_Rmin = Parts_Scale(self.rgb_frame)
        self.scale_Rmin.configure(label='R_min', side='top', from_=0, to=255)
        self.scale_Rmax = Parts_Scale(self.rgb_frame)
        self.scale_Rmax.configure(label='R_max', side='top', from_=0, to=255)
        self.scale_Gmin = Parts_Scale(self.rgb_frame)
        self.scale_Gmin.configure(label='G_min', side='top', from_=0, to=255)
        self.scale_Gmax = Parts_Scale(self.rgb_frame)
        self.scale_Gmax.configure(label='G_max', side='top', from_=0, to=255)
        self.scale_Bmin = Parts_Scale(self.rgb_frame)
        self.scale_Bmin.configure(label='B_min', side='top', from_=0, to=255)
        self.scale_Bmax = Parts_Scale(self.rgb_frame)
        self.scale_Bmax.configure(label='B_max', side='top', from_=0, to=255)
        self.rgb_frame.pack(fill="x", side="top")
        self.hsv_frame = tk.LabelFrame(self.settings_frame)
        self.hsv_frame.configure(height=200, text='HSV', width=200)
        self.scale_Hmin = Parts_Scale(self.hsv_frame)
        self.scale_Hmin.configure(label='H_min', side='top', from_=0, to=255)
        self.scale_Hmax = Parts_Scale(self.hsv_frame)
        self.scale_Hmax.configure(label='H_max', side='top', from_=0, to=255)
        self.scale_Smin = Parts_Scale(self.hsv_frame)
        self.scale_Smin.configure(label='S_min', side='top', from_=0, to=255)
        self.scale_Smax = Parts_Scale(self.hsv_frame)
        self.scale_Smax.configure(label='S_max', side='top', from_=0, to=255)
        self.scale_Vmin = Parts_Scale(self.hsv_frame)
        self.scale_Vmin.configure(label='V_min', side='top', from_=0, to=255)
        self.scale_Vmax = Parts_Scale(self.hsv_frame)
        self.scale_Vmax.configure(label='V_max', side='top', from_=0, to=255)
        self.hsv_frame.pack(side="top")

        if not self.__flag:
            self.__show_mode(0)
            self.var.set(0)
            self.scale_Rmin.set(self.__P1min)
            self.scale_Rmax.set(self.__P1max)
            self.scale_Gmin.set(self.__P2min)
            self.scale_Gmax.set(self.__P2max)
            self.scale_Bmin.set(self.__P3min)
            self.scale_Bmax.set(self.__P3max)
            self.scale_Hmax.set(255)
            self.scale_Smax.set(255)
            self.scale_Vmax.set(255)
        else:
            self.__show_mode(1)
            self.var.set(1)
            self.scale_Hmin.set(self.__P1min)
            self.scale_Hmax.set(self.__P1max)
            self.scale_Smin.set(self.__P2min)
            self.scale_Smax.set(self.__P2max)
            self.scale_Vmin.set(self.__P3min)
            self.scale_Vmax.set(self.__P3max)
            self.scale_Rmax.set(255)
            self.scale_Gmax.set(255)
            self.scale_Bmax.set(255)

    def __init_events(self):
        self.radiobutton1.configure(command=self.__onClick_optbtn)
        self.radiobutton2.configure(command=self.__onClick_optbtn)
        self.scale_Rmin.bind(changed=self.__onScale)
        self.scale_Rmax.bind(changed=self.__onScale)
        self.scale_Gmin.bind(changed=self.__onScale)
        self.scale_Gmax.bind(changed=self.__onScale)
        self.scale_Bmin.bind(changed=self.__onScale)
        self.scale_Bmax.bind(changed=self.__onScale)

        self.scale_Hmin.bind(changed=self.__onScale)
        self.scale_Hmax.bind(changed=self.__onScale)
        self.scale_Smin.bind(changed=self.__onScale)
        self.scale_Smax.bind(changed=self.__onScale)
        self.scale_Vmin.bind(changed=self.__onScale)
        self.scale_Vmax.bind(changed=self.__onScale)

    def __onClick_optbtn(self):
        mode = self.var.get()
        if mode == 0:
            self.__flag = False
        else:
            self.__flag = True
        self.__show_mode(mode)
        self.__get_param_val(mode)
        self.dst_img = self.__inrange()
        self.Draw()

    def __get_param_val(self, mode):
        if mode == 0:
            self.__P1min = self.scale_Rmin.get()
            self.__P1max = self.scale_Rmax.get()
            self.__P2min = self.scale_Gmin.get()
            self.__P2max = self.scale_Gmax.get()
            self.__P3min = self.scale_Bmin.get()
            self.__P3max = self.scale_Bmax.get()
        else:
            self.__P1min = self.scale_Hmin.get()
            self.__P1max = self.scale_Hmax.get()
            self.__P2min = self.scale_Smin.get()
            self.__P2max = self.scale_Smax.get()
            self.__P3min = self.scale_Vmin.get()
            self.__P3max = self.scale_Vmax.get()

    def __onScale(self):
        if self.__proc_flag:
            return
        self.__proc_flag = True
        self.__get_param_val(self.var.get())
        self.dst_img = self.__inrange()
        self.Draw()
        self.__proc_flag = False

    def __show_mode(self, mode):
        if mode == 0:
            self.hsv_frame.pack_forget()
            self.rgb_frame.pack()
        else:
            self.rgb_frame.pack_forget()
            self.hsv_frame.pack()
            pass

    def __inrange(self):
        img_copy = self.origin_img.copy()

        if not self.__flag:
            img_copy = cv2.inRange(img_copy,
                                   (self.__P3min, self.__P2min, self.__P1min),
                                   (self.__P3max, self.__P2max, self.__P1max))
        else:
            img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV_FULL)
            H_low = self.__P1min
            H_high = self.__P1max
            S_low = self.__P2min
            S_high = self.__P2max
            V_low = self.__P3min
            V_high = self.__P3max

            if H_low > H_high:
                lower_color1 = np.array([H_low, S_low, V_low])
                upper_color1 = np.array([255, S_high, V_high])
                # 指定した範囲内を白、それ以外を黒にする（マスク画像の生成
                mask1 = cv2.inRange(img_copy, lower_color1, upper_color1)
                # 取得する色の範囲を指定する
                lower_color2 = np.array([0, S_low, V_low])
                upper_color2 = np.array([H_high, S_high, V_high])
                # 指定した範囲内を白、それ以外を黒にする（マスク画像の生成
                mask2 = cv2.inRange(img_copy, lower_color2, upper_color2)
                # マスクの結合
                img_copy = mask1 + mask2
            else:
                # 取得する色の範囲を指定する
                lower_color = np.array([H_low, S_low, V_low])
                upper_color = np.array([H_high, S_high, V_high])
                # 指定した範囲内を白、それ以外を黒にする（マスク画像の生成
                img_copy = cv2.inRange(img_copy, lower_color, upper_color)
        return img_copy

    def get_data(self):
        param = []
        param.append(self.__P1min)
        param.append(self.__P1max)
        param.append(self.__P2min)
        param.append(self.__P2max)
        param.append(self.__P3min)
        param.append(self.__P3max)
        param.append(self.__flag)

        img = self.dst_img
        if len(self.dst_img.shape) == 2:
            img = cv2.cvtColor(self.dst_img, cv2.COLOR_GRAY2BGR)
        if self.__gui:
            print('Proc : inRange')
            print(f'param = {param}')
        return param, img


if __name__ == "__main__":
    # img = cv2.imread('./0000_img/I.jpg')
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    # param = [0, 161, 184, 255, 0, 255, False]   # RGB
    # param = [191, 49, 191, 255, 191, 255, True]  # HSV
    app = InRange(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./inrange.jpg', dst_img)
