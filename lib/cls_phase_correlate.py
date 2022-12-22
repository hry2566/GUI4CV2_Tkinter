"""位置合わせ"""
import os
import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class PhaseCorrelate(EditWindow):
    """位置合わせクラス"""

    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.base_img_path = ''
        self.__proc_flag = False
        self.__gui = gui

        if len(param) == 1:
            self.base_img_path = param[0]
        else:
            pass

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__phase_correlate()

        if gui:
            self.draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.button1 = tk.Button(self.settings_frame)
        self.button1.configure(text='select base file',
                               command=self.__btn1_click)
        self.button1.pack(anchor='w', side='top')
        self.entry1 = tk.Entry(self.settings_frame)
        self.entry1.configure(width='30')
        self.entry1.pack(fill='x', side='top')

        self.entry1.delete('0', 'end')
        self.entry1.insert('0', self.base_img_path)

    def __open_file(self):
        root = tk.Tk()
        root.withdraw()
        typ = [('', '*')]
        directory = './'
        file = filedialog.askopenfilenames(
            filetypes=typ, initialdir=directory)
        root.destroy()
        if len(file) == 0:
            path = ''
        else:
            path = file[0]

        path = path.replace('\\', '/')
        cur_dir = os.getcwd().replace('\\', '/')
        path = path.replace(cur_dir, '.')
        return path

    def __btn1_click(self):
        if self.__proc_flag:
            return
        self.__proc_flag = True
        path = self.__open_file()

        if path != '':
            self.base_img_path = path
            self.entry1.delete('0', 'end')
            self.entry1.insert('0', self.base_img_path)
            self.dst_img = self.__phase_correlate()
            self.draw()
        self.__proc_flag = False

    def __init_events(self):
        pass

    # def __onScale(self, events):
    #     pass

    def __ripoc(self, base, dist, m=None):
        g_a = np.asarray(cv2.cvtColor(base, cv2.COLOR_BGR2GRAY), 'float')
        g_b = np.asarray(cv2.cvtColor(dist, cv2.COLOR_BGR2GRAY), 'float')

        height, width = g_a.shape
        han_y = np.hanning(height)
        han_x = np.hanning(width)
        han_w = han_y.reshape(height, 1)*han_x

        f_a = np.fft.fftshift(np.log(np.abs(np.fft.fft2(g_a*han_w))))
        f_b = np.fft.fftshift(np.log(np.abs(np.fft.fft2(g_b*han_w))))

        if not m:
            l = np.sqrt(width*width + height*height)
            m = l/np.log(l)

        center = (width/2, height/2)
        flags = cv2.INTER_LANCZOS4 + cv2.WARP_POLAR_LOG
        p_a = cv2.warpPolar(f_a, (width, height), center, m, flags)
        p_b = cv2.warpPolar(f_b, (width, height), center, m, flags)
        (pos_x, pos_y), _ = cv2.phaseCorrelate(p_a, p_b, han_w)

        angle = pos_y*360/height
        scale = (np.e)**(pos_x/m)
        matrix = cv2.getRotationMatrix2D(center, angle, scale)
        t_b = cv2.warpAffine((g_b), matrix, (width, height))
        (pos_x, pos_y), _ = cv2.phaseCorrelate(g_a, t_b)
        return pos_x, pos_y, angle, scale

    def __phase_correlate(self):
        img_copy = self.origin_img.copy()

        if self.base_img_path == '':
            img = img_copy
        else:
            base_img = cv2.imread(self.base_img_path)
            pos_x, pos_y, angle, scale = self.__ripoc(base_img, img_copy)
            scale = 1.0
            height, width, _ = img_copy.shape

            matrix = cv2.getRotationMatrix2D((width/2, height/2), angle, scale)
            matrix[0][2] -= pos_x
            matrix[1][2] -= pos_y

            img = cv2.warpAffine(img_copy, matrix, (width, height))
        return img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.base_img_path)
        if self.__gui:
            print('Proc : PhaseCorrelate')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     img = cv2.imread('./0000_img/ECU/ECUlow_2.jpg')
#     # img = cv2.imread('./0000_img/ECU/rotate2.jpg')
#     param = ['./0000_img/ECU/ECUlow_base.jpg']
#     # param = []
#     app = PhaseCorrelate(img, param, gui=False)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./PhaseCorrelate.jpg', dst_img)
