import math
import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class CircleDetection(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        if not len(img) == 2:
            self.dst_img = img
            return

        self.origin_img = img[0]
        self.__mask_img = img[1]
        img = img[0]
        self.__draw_corcle = False
        self.__draw_edge = True
        self.__image_bond = False
        self.__circle_info = []
        self.__gui = gui

        # self.__proc_flag = False

        if len(param) == 4:
            self.__draw_corcle = param[0]
            self.__draw_edge = param[1]
            self.__image_bond = param[2]
            pass
        else:
            pass

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__circle_detection()

        if gui:
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.bln1 = tk.BooleanVar()
        self.bln1.set(False)
        self.bln2 = tk.BooleanVar()
        self.bln2.set(True)
        self.bln3 = tk.BooleanVar()
        self.bln3.set(False)

        self.frame1 = tk.Frame(self.settings_frame)
        self.frame1.configure(height=200, width=200)
        self.checkbutton1 = tk.Checkbutton(self.frame1, variable=self.bln1)
        self.checkbutton1.configure(
            text='reference circle', command=self.__onClick_check)
        self.checkbutton1.pack(anchor="w", side="top")
        self.checkbutton2 = tk.Checkbutton(self.frame1, variable=self.bln2)
        self.checkbutton2.configure(text='edge', command=self.__onClick_check)
        self.checkbutton2.pack(anchor="w", side="top")
        self.checkbutton3 = tk.Checkbutton(self.frame1, variable=self.bln3)
        self.checkbutton3.configure(
            text='image synthesis', command=self.__onClick_check)
        self.checkbutton3.pack(anchor="w", side="top")
        self.frame1.pack(side="top")

        self.labelframe1 = tk.LabelFrame(self.frame1)
        self.labelframe1.configure(height=200, text='pixel', width=200)
        self.frame3 = tk.Frame(self.labelframe1)
        self.frame3.configure(height=200, width=200)
        self.label2 = tk.Label(self.frame3)
        self.label2.configure(text='center', width=6)
        self.label2.pack(side="left")
        self.entry_center = tk.Entry(self.frame3)
        self.entry_center.configure(width=10)
        self.entry_center.pack(side="top")
        self.frame3.pack(fill="x", side="top")
        self.frame4 = tk.Frame(self.labelframe1)
        self.frame4.configure(height=200, width=200)
        self.label3 = tk.Label(self.frame4)
        self.label3.configure(text='radius', width=6)
        self.label3.pack(side="left")
        self.entry_radius = tk.Entry(self.frame4)
        self.entry_radius.configure(width=10)
        self.entry_radius.pack(side="top")
        self.frame4.pack(fill="x", side="top")
        self.labelframe1.pack(fill="x", padx=5, pady=5, side="top")
        self.frame1.pack(fill="x", side="top")

        self.bln1.set(self.__draw_corcle)
        self.bln2.set(self.__draw_edge)
        self.bln3.set(self.__image_bond)

    def __init_events(self):
        pass

    def __onScale(self, events):
        pass

    def __onClick_check(self):
        self.__draw_corcle = self.bln1.get()
        self.__draw_edge = self.bln2.get()
        self.__image_bond = self.bln3.get()

        self.dst_img = self.__circle_detection()
        self.Draw()

    def __circle_detection(self):
        img_origin = self.origin_img.copy()
        img_copy = self.__mask_img.copy()
        img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        img_gray = cv2.bitwise_not(img_gray)

        contours, _ = cv2.findContours(
            img_gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        cnt = np.asarray(0)

        for i in range(len(contours)):
            contour_i = contours[i]
            contour_count = np.sum(contour_i.shape)
            if contour_count > np.sum(cnt.shape):
                cnt = contour_i

        # 外接円
        (x, y), rad = cv2.minEnclosingCircle(cnt)
        center = (int(x), int(y))
        rad_int = int(rad)
        self.__circle_info = []
        self.__circle_info.append(center)
        self.__circle_info.append(rad_int)

        if self.__gui:
            self.entry_center.delete(0, tk.END)
            self.entry_center.insert(0, f'{center[0]}, {center[1]}')
            self.entry_radius.delete(0, tk.END)
            self.entry_radius.insert(0, rad_int)

        if not self.__image_bond:
            if self.__draw_edge:
                img_origin = cv2.drawContours(
                    img_origin, [cnt], 0, (0, 0, 255), 3)

            if self.__draw_corcle:
                img_origin = cv2.circle(
                    img_origin, center, rad_int, (255, 0, 0), 3)
        else:
            zero = np.zeros(img_origin.shape, dtype="uint8")
            # img_origin = cv2.circle(
            #     zero, center, rad_int, (255, 255, 255), -1)
            ellipse = cv2.fitEllipse(cnt)
            img_origin = cv2.ellipse(zero, ellipse, (255, 255, 255), -1)

            img_origin = cv2.drawContours(
                img_origin, [cnt], 0, (0, 0, 0), -1)

        return img_origin

    def get_distance(self, x1, y1, x2, y2):
        d = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        return d

    def get_data(self):
        param = []
        param.append(self.__draw_corcle)
        param.append(self.__draw_edge)
        param.append(self.__image_bond)
        param.append(self.__circle_info)
        print('Proc : CircleDetection')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img_base = cv2.imread('./0000_img/ECU/ECUlow_1.jpg')
    mask_img = cv2.imread('./circle1.png')
    img = [img_base, mask_img]
    param = [False, False, True, []]
    app = CircleDetection(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./CircleDetection.jpg', dst_img)
