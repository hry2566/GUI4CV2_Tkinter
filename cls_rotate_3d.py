import math
import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class Rotate3D(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__axis_x = 0
        self.__axis_y = 0
        self.__axis_z = 0
        self.__pos1_z = 0
        self.__pos2_z = 0
        self.__pos3_z = 0
        self.__pos4_z = 0
        height, width = img.shape[:2]
        self.__p1 = [0, 0, 0]
        self.__p2 = [width, 0, 0]
        self.__p3 = [0, height, 0]
        self.__p4 = [width, height, 0]
        self.__set_mode = 0
        self.__proc_flag = False
        self.cnt = 0

        if len(param) == 11:
            self.__p1 = param[0]
            self.__p2 = param[1]
            self.__p3 = param[2]
            self.__p4 = param[3]
            self.__axis_x = param[4]
            self.__axis_y = param[5]
            self.__axis_z = param[6]
            self.__pos1_z = param[7]
            self.__pos2_z = param[8]
            self.__pos3_z = param[9]
            self.__pos4_z = param[10]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()
            self.run()
        else:
            self.dst_img = self.__rotate_3d()

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
        self.setbtn1.configure(text='set', command=self.__onBtn1Click)
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
        self.setbtn2.configure(text='set', command=self.__onBtn2Click)
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
        self.setbtn3.configure(text='set', command=self.__onBtn3Click)
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
        self.setbtn4.configure(text='set', command=self.__onBtn4Click)
        self.setbtn4.pack(expand='true', fill='x', side='left')
        self.labelframe4.configure(
            height='200', text='right_bottom (x, y)', width='200')
        self.labelframe4.pack(fill='x', padx='5', pady='5', side='top')

        self.__scale1 = tk.Scale(self.settings_frame)
        self.__scale1.configure(from_=-90, to=90,
                                label="axis x", orient="horizontal", command=self.__onScale)
        self.__scale1.pack(side="top")

        self.__scale2 = tk.Scale(self.settings_frame)
        self.__scale2.configure(from_=-90, to=90,
                                label="axis y", orient="horizontal", command=self.__onScale)
        self.__scale2.pack(side="top")

        self.__scale3 = tk.Scale(self.settings_frame)
        self.__scale3.configure(from_=-90, to=90,
                                label="axis z", orient="horizontal", command=self.__onScale)
        self.__scale3.pack(side="top")

        self.__scale4 = tk.Scale(self.settings_frame)
        self.__scale4.configure(from_=-100, to=100,
                                label="pos1 z", orient="horizontal", command=self.__onScale)
        self.__scale4.pack(side="top")

        self.__scale5 = tk.Scale(self.settings_frame)
        self.__scale5.configure(from_=-100, to=100,
                                label="pos2 z", orient="horizontal", command=self.__onScale)
        self.__scale5.pack(side="top")

        self.__scale6 = tk.Scale(self.settings_frame)
        self.__scale6.configure(from_=-100, to=100,
                                label="pos3 z", orient="horizontal", command=self.__onScale)
        self.__scale6.pack(side="top")

        self.__scale7 = tk.Scale(self.settings_frame)
        self.__scale7.configure(from_=-100, to=100,
                                label="pos4 z", orient="horizontal", command=self.__onScale)
        self.__scale7.pack(side="top")

        self.setbtn5 = tk.Button(self.settings_frame)
        self.setbtn5.configure(text='reset', command=self.__onBtn5Click)
        self.setbtn5.pack(expand='true', fill='x', side='left')

        self.entry1.delete('0', 'end')
        self.entry1.insert('0', f'({self.__p1[0]},{self.__p1[1]})')
        self.entry2.delete('0', 'end')
        self.entry2.insert('0', f'({self.__p2[0]},{self.__p2[1]})')
        self.entry3.delete('0', 'end')
        self.entry3.insert('0', f'({self.__p3[0]},{self.__p3[1]})')
        self.entry4.delete('0', 'end')
        self.entry4.insert('0', f'({self.__p4[0]},{self.__p4[1]})')

        self.__scale1.set(self.__axis_x)
        self.__scale2.set(self.__axis_y)
        self.__scale3.set(self.__axis_z)
        self.__scale4.set(self.__pos1_z)
        self.__scale5.set(self.__pos2_z)
        self.__scale6.set(self.__pos3_z)
        self.__scale7.set(self.__pos4_z)
        pass

    def __init_events(self):
        self.canvas1.bind("<1>", self.__OnClick)
        pass

    def __onBtn1Click(self):
        self.__set_mode = 0

    def __onBtn2Click(self):
        self.__set_mode = 1

    def __onBtn3Click(self):
        self.__set_mode = 2

    def __onBtn4Click(self):
        self.__set_mode = 3

    def __onBtn5Click(self):
        self.__axis_x = 0
        self.__axis_y = 0
        self.__axis_z = 0
        self.__pos2_z = 0
        self.__pos3_z = 0
        self.__pos4_z = 0
        self.__scale1.set(0)
        self.__scale2.set(0)
        self.__scale3.set(0)
        self.__scale4.set(0)
        self.__scale5.set(0)
        self.__scale6.set(0)
        self.__scale7.set(0)

        pass

    def __GetMousePos(self, pos):
        view_scale = self.GetViewScale()
        canvas_width = int(self.canvas1.winfo_width()*view_scale)
        canvas_height = int(self.canvas1.winfo_height()*view_scale)

        img_width = self.origin_img.shape[1]
        img_height = self.origin_img.shape[0]

        scale_x = img_width/canvas_width
        scale_y = img_height/canvas_height
        pos_x, pos_y = self.GetImgPos()

        if scale_x < scale_y:
            scale = scale_y
            dev = int((canvas_width-img_width/scale)/2)
            x = int((pos.x-dev)*scale)-int(pos_x*scale)
            y = int(pos.y*scale)-int(pos_y*scale)
        else:
            scale = scale_x
            dev = int((canvas_height-img_height/scale)/2)
            x = int(pos.x*scale)-int(pos_x*scale)
            y = int((pos.y-dev)*scale)-int(pos_y*scale)

        return x, y

    def __OnClick(self, event):
        x, y = self.__GetMousePos(event)

        if self.__set_mode == 0:
            self.entry1.delete('0', 'end')
            self.entry1.insert('0', f'({x},{y})')
            self.__p1[0] = x
            self.__p1[1] = y
        elif self.__set_mode == 1:
            self.entry2.delete('0', 'end')
            self.entry2.insert('0', f'({x},{y})')
            self.__p2[0] = x
            self.__p2[1] = y
        elif self.__set_mode == 2:
            self.entry3.delete('0', 'end')
            self.entry3.insert('0', f'({x},{y})')
            self.__p3[0] = x
            self.__p3[1] = y
        elif self.__set_mode == 3:
            self.entry4.delete('0', 'end')
            self.entry4.insert('0', f'({x},{y})')
            self.__p4[0] = x
            self.__p4[1] = y

    def __onScale(self, events):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__axis_x = self.__scale1.get()
        self.__axis_y = self.__scale2.get()
        self.__axis_z = self.__scale3.get()
        self.__pos1_z = self.__scale4.get()
        self.__pos2_z = self.__scale5.get()
        self.__pos3_z = self.__scale6.get()
        self.__pos4_z = self.__scale7.get()

        self.dst_img = self.__rotate_3d()
        self.Draw()
        self.__proc_flag = False
        pass

    def __rotate_x(self, pos, ang):
        p = pos.copy()
        angX = math.radians(ang[0])
        angY = math.radians(ang[1])
        angZ = math.radians(ang[2])
        p[0] = self.__x_X(angX, p)
        p[0] = self.__x_Y(angY, p)
        p[0] = self.__x_Z(angZ, p)
        return p[0]

    def __x_X(self, angX, pos):
        x = pos[0]
        y = pos[1]
        z = pos[2]
        return 1 * x + 0 * y + 0 * z

    def __x_Y(self, angY, pos):
        x = pos[0]
        y = pos[1]
        z = pos[2]
        return math.cos(angY) * x + 0 * y + math.sin(angY) * z

    def __x_Z(self, angZ, pos):
        x = pos[0]
        y = pos[1]
        z = pos[2]
        return math.cos(angZ) * x + -1 * math.sin(angZ) * y + 0 * z

    def __rotate_y(self, pos, ang):
        p = pos.copy()
        angX = math.radians(ang[0])
        angY = math.radians(ang[1])
        angZ = math.radians(ang[2])
        p[1] = self.__y_X(angX, p)
        p[1] = self.__y_Y(angY, p)
        p[1] = self.__y_Z(angZ, p)
        return p[1]

    def __y_X(self, angX, pos):
        x = pos[0]
        y = pos[1]
        z = pos[2]
        return 0 * x + math.cos(angX) * y + -1 * math.sin(angX) * z

    def __y_Y(self, angY, pos):
        x = pos[0]
        y = pos[1]
        z = pos[2]
        return 0 * x + 1 * y + 0 * z

    def __y_Z(self, angZ, pos):
        x = pos[0]
        y = pos[1]
        z = pos[2]
        return math.sin(angZ) * x + math.cos(angZ) * y + 0 * z

    def __rotate_3d(self):
        img = self.origin_img.copy()

        axis = [self.__axis_x, self.__axis_y, self.__axis_z]
        center_x = (self.__p1[0]+self.__p4[0])/2
        center_y = (self.__p1[1]+self.__p4[1])/2
        center_p1 = [self.__p1[0]-center_x,
                     self.__p1[1]-center_y,
                     self.__pos1_z]
        center_p2 = [self.__p2[0]-center_x,
                     self.__p2[1]-center_y,
                     self.__pos2_z]
        center_p3 = [self.__p3[0]-center_x,
                     self.__p3[1]-center_y,
                     self.__pos3_z]
        center_p4 = [self.__p4[0]-center_x,
                     self.__p4[1]-center_y,
                     self.__pos4_z]

        x1 = self.__rotate_x(center_p1, axis) + center_x
        y1 = self.__rotate_y(center_p1, axis) + center_y
        x2 = self.__rotate_x(center_p2, axis) + center_x
        y2 = self.__rotate_y(center_p2, axis) + center_y
        x3 = self.__rotate_x(center_p3, axis) + center_x
        y3 = self.__rotate_y(center_p3, axis) + center_y
        x4 = self.__rotate_x(center_p4, axis) + center_x
        y4 = self.__rotate_y(center_p4, axis) + center_y

        # # 変換前の4点
        p1 = np.array([self.__p1[0], self.__p1[1]])
        p2 = np.array([self.__p2[0], self.__p2[1]])
        p3 = np.array([self.__p3[0], self.__p3[1]])
        p4 = np.array([self.__p4[0], self.__p4[1]])

        src_pts = np.array([[p1[0], p1[1]],
                            [p2[0], p2[1]],
                            [p3[0], p3[1]],
                            [p4[0], p4[1]]],
                           dtype=np.float32)
        dst_pts = np.array([[x1, y1],
                            [x2, y2],
                            [x3, y3],
                            [x4, y4]],
                           dtype=np.float32)

        # mat = cv2.getAffineTransform(src_pts, dst_pts)
        mat = cv2.getPerspectiveTransform(src_pts, dst_pts)

        # img = cv2.warpAffine(img, mat, (img.shape[1], img.shape[0]))
        img = cv2.warpPerspective(img, mat, (img.shape[1], img.shape[0]))

        return img

    def get_data(self):
        param = []
        param.append(self.__p1)
        param.append(self.__p2)
        param.append(self.__p3)
        param.append(self.__p4)

        param.append(self.__axis_x)
        param.append(self.__axis_y)
        param.append(self.__axis_z)

        param.append(self.__pos1_z)
        param.append(self.__pos2_z)
        param.append(self.__pos3_z)
        param.append(self.__pos4_z)

        # param.append(self.__kernel_y)
        print('Proc : Rotate3D')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    # img = cv2.imread('./0000_img/opencv_logo.jpg')
    img = cv2.imread('./0000_img/20.png')
    param = []
    param = [[46, 158, 0], [421, 64, 0], [37, 247, 0],
             [427, 172, 0], -48, 18, 0, -36, 61, -10, 53]

    # param = [[290, -71, 0], [421, 64, 0], [37, 247, 0],
    #          [427, 172, 0], 41, 23, 12, 30, 58, 56, 100]

    app = Rotate3D(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./Rotate3D.jpg', dst_img)
