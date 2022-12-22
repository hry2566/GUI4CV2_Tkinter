"""射影変形"""
import math
import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow
from lib.parts.parts_scale import Parts_Scale


class Rotate3D(EditWindow):
    """射影変形クラス"""

    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__img_bk = img
        height, width = img.shape[:2]
        self.__p1 = [0, 0, 0]
        self.__p2 = [width, 0, 0]
        self.__p3 = [0, height, 0]
        self.__p4 = [width, height, 0]
        self.__w_ratio = 1.0
        self.__set_mode = 0
        self.cnt = 0
        self.__gui = gui

        if len(param) == 5:
            self.__p1 = param[0]
            self.__p2 = param[1]
            self.__p3 = param[2]
            self.__p4 = param[3]
            self.__w_ratio = param[4]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__rotate_3d()

        if gui:
            self.draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.frame1 = tk.Frame(self.settings_frame)
        self.entry1 = tk.Entry(self.frame1)

        self.labelframe1 = tk.LabelFrame(self.settings_frame)
        self.entry1 = tk.Entry(self.labelframe1)
        self.entry1.configure(width='10')
        _text_ = '''0'''
        self.entry1.delete('0', 'end')
        self.entry1.insert('0', _text_)
        self.entry1.pack(side='left')
        self.setbtn1 = tk.Button(self.labelframe1)
        self.setbtn1.configure(text='set', command=self.__on_btn1_click)
        self.setbtn1.pack(expand='true', fill='x', side='left')
        self.labelframe1.configure(
            height='200', text='left_top (x, y)', width='200')
        self.labelframe1.pack(fill='x', padx='5', pady='5', side='top')

        self.labelframe2 = tk.LabelFrame(self.settings_frame)
        self.entry2 = tk.Entry(self.labelframe2)
        self.entry2.configure(width='10')
        _text_ = '''0'''
        self.entry2.delete('0', 'end')
        self.entry2.insert('0', _text_)
        self.entry2.pack(side='left')
        self.setbtn2 = tk.Button(self.labelframe2)
        self.setbtn2.configure(text='set', command=self.__on_btn2_click)
        self.setbtn2.pack(expand='true', fill='x', side='left')
        self.labelframe2.configure(
            height='200', text='right_top (x, y)', width='200')
        self.labelframe2.pack(fill='x', padx='5', pady='5', side='top')

        self.labelframe3 = tk.LabelFrame(self.settings_frame)
        self.entry3 = tk.Entry(self.labelframe3)
        self.entry3.configure(width='10')
        _text_ = '''0'''
        self.entry3.delete('0', 'end')
        self.entry3.insert('0', _text_)
        self.entry3.pack(side='left')
        self.setbtn3 = tk.Button(self.labelframe3)
        self.setbtn3.configure(text='set', command=self.__on_btn3_click)
        self.setbtn3.pack(expand='true', fill='x', side='left')
        self.labelframe3.configure(
            height='200', text='left_bottom (x, y)', width='200')
        self.labelframe3.pack(fill='x', padx='5', pady='5', side='top')

        self.labelframe4 = tk.LabelFrame(self.settings_frame)
        self.entry4 = tk.Entry(self.labelframe4)
        self.entry4.configure(width='10')
        _text_ = '''0'''
        self.entry4.delete('0', 'end')
        self.entry4.insert('0', _text_)
        self.entry4.pack(side='left')
        self.setbtn4 = tk.Button(self.labelframe4)
        self.setbtn4.configure(text='set', command=self.__on_btn4_click)
        self.setbtn4.pack(expand='true', fill='x', side='left')
        self.labelframe4.configure(
            height='200', text='right_bottom (x, y)', width='200')
        self.labelframe4.pack(fill='x', padx='5', pady='5', side='top')
        self.labelframe5 = tk.LabelFrame(self.settings_frame)
        self.__scale1 = Parts_Scale(self.labelframe5)
        self.__scale1.configure(
            label='ratio_xy', side='top', resolution=0.01, from_=0.1, to=5)
        self.setbtn5 = tk.Button(self.labelframe5)
        self.setbtn5.configure(text='show', command=self.__on_btn5_click)
        self.setbtn5.pack(expand='true', fill='x', side='top')
        self.labelframe5.configure(
            height='200', text='view', width='200')
        self.labelframe5.pack(fill='x', padx='5', pady='5', side='top')

        self.entry1.delete('0', 'end')
        self.entry1.insert('0', f'({self.__p1[0]},{self.__p1[1]})')
        self.entry2.delete('0', 'end')
        self.entry2.insert('0', f'({self.__p2[0]},{self.__p2[1]})')
        self.entry3.delete('0', 'end')
        self.entry3.insert('0', f'({self.__p3[0]},{self.__p3[1]})')
        self.entry4.delete('0', 'end')
        self.entry4.insert('0', f'({self.__p4[0]},{self.__p4[1]})')
        self.__scale1.set(self.__w_ratio)

    def __init_events(self):
        self.canvas1.bind("<1>", self.__on_click)
        self.__scale1.bind(changed=self.__on_scale)

    def __on_btn1_click(self):
        self.__set_mode = 0

    def __on_btn2_click(self):
        self.__set_mode = 1

    def __on_btn3_click(self):
        self.__set_mode = 2

    def __on_btn4_click(self):
        self.__set_mode = 3

    def __on_btn5_click(self):
        self.dst_img = self.__rotate_3d()
        self.draw()

    def __get_mouse_pos(self, pos):
        view_scale = self.get_view_scale()
        canvas_width = int(self.canvas1.winfo_width()*view_scale)
        canvas_height = int(self.canvas1.winfo_height()*view_scale)

        img_width = self.origin_img.shape[1]
        img_height = self.origin_img.shape[0]

        scale_x = img_width/canvas_width
        scale_y = img_height/canvas_height
        pos_x, pos_y = self.get_img_pos()

        if scale_x < scale_y:
            scale = scale_y
            dev = int((canvas_width-img_width/scale)/2)
            pos_x = int((pos.x-dev)*scale)-int(pos_x*scale)
            pos_y = int(pos.y*scale)-int(pos_y*scale)
        else:
            scale = scale_x
            dev = int((canvas_height-img_height/scale)/2)
            pos_x = int(pos.x*scale)-int(pos_x*scale)
            pos_y = int((pos.y-dev)*scale)-int(pos_y*scale)

        return pos_x, pos_y

    def __on_click(self, event):
        pos_x, pos_y = self.__get_mouse_pos(event)

        if self.__set_mode == 0:
            self.entry1.delete('0', 'end')
            self.entry1.insert('0', f'({pos_x},{pos_y})')
            self.__p1[0] = pos_x
            self.__p1[1] = pos_y

        elif self.__set_mode == 1:
            self.entry2.delete('0', 'end')
            self.entry2.insert('0', f'({pos_x},{pos_y})')
            self.__p2[0] = pos_x
            self.__p2[1] = pos_y
        elif self.__set_mode == 2:
            self.entry3.delete('0', 'end')
            self.entry3.insert('0', f'({pos_x},{pos_y})')
            self.__p3[0] = pos_x
            self.__p3[1] = pos_y
        elif self.__set_mode == 3:
            self.entry4.delete('0', 'end')
            self.entry4.insert('0', f'({pos_x},{pos_y})')
            self.__p4[0] = pos_x
            self.__p4[1] = pos_y

        img = self.__img_bk.copy()

        cv2.circle(img, (self.__p1[0], self.__p1[1]),
                   5, (0, 0, 255), thickness=-1)
        cv2.circle(img, (self.__p2[0], self.__p2[1]),
                   5, (0, 255, 0), thickness=-1)
        cv2.circle(img, (self.__p3[0], self.__p3[1]),
                   5, (255, 0, 0), thickness=-1)
        cv2.circle(img, (self.__p4[0], self.__p4[1]),
                   5, (0, 0, 0), thickness=-1)

        self.dst_img = img
        self.draw()

    def __on_scale(self):
        self.__w_ratio = self.__scale1.get()
        self.dst_img = self.__rotate_3d()
        self.draw()

    def __rotate_3d(self):
        img = self.__img_bk.copy()
        rows, cols = img.shape[:2]
        w_ratio = self.__w_ratio

        p_1 = np.array([self.__p1[0], self.__p1[1]])
        p_2 = np.array([self.__p2[0], self.__p2[1]])
        p_3 = np.array([self.__p3[0], self.__p3[1]])
        p_4 = np.array([self.__p4[0], self.__p4[1]])

        pts1 = np.float32([p_1, p_2, p_3, p_4])

        #　幅取得
        o_width = np.linalg.norm(p_2 - p_1)
        o_width = math.floor(o_width * w_ratio)

        #　高さ取得
        o_height = np.linalg.norm(p_3 - p_1)
        o_height = math.floor(o_height)

        # 変換後の4点
        pts2 = np.float32([[0+p_1[0], 0+p_1[1]],
                          [o_width+p_1[0], 0+p_1[1]],
                          [0+p_1[0], o_height+p_1[1]],
                          [o_width+p_1[0], o_height+p_1[1]]])

        matrix = cv2.getPerspectiveTransform(pts1, pts2)
        img = cv2.warpPerspective(img, matrix, (cols, rows))

        return img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.__p1)
        param.append(self.__p2)
        param.append(self.__p3)
        param.append(self.__p4)
        param.append(self.__w_ratio)

        if self.__gui:
            print('Proc : Rotate3D')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     # img = cv2.imread('./0000_img/opencv_logo.jpg')
#     img = cv2.imread('./0000_img/20.png')
#     param = []

#     param = [[45, 158], [421, 63], [36, 247], [427, 174], 1.0]

#     app = Rotate3D(img, param, gui=False)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./Rotate3D.jpg', dst_img)
