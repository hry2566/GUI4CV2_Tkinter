"""位置合わせ(PhaseCorrelate_XY)"""
import os
import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class PhaseCorrelateXY(EditWindow):
    """位置合わせ(PhaseCorrelate_XY)クラス"""

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

        self.dst_img = self.__phase_correlate_xy()

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
            self.dst_img = self.__phase_correlate_xy()
            self.draw()
        self.__proc_flag = False

    def __init_events(self):
        pass

    # def __onScale(self, events):
    #     pass

    def __phase_correlate_xy(self):
        img_copy = self.origin_img.copy()
        img_copy_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        img_copy_float = np.float32(img_copy_gray)

        if self.base_img_path == '':
            img = img_copy
        else:
            height, width, _ = img_copy.shape
            base_img = cv2.imread(self.base_img_path)
            base_img = cv2.cvtColor(base_img, cv2.COLOR_BGR2GRAY)
            base_img_float = np.float32(base_img)
            distance, _ = cv2.phaseCorrelate(img_copy_float, base_img_float)
            distance_x, distance_y = distance
            matrix = np.float32([[1, 0, distance_x], [0, 1, distance_y]])
            img = cv2.warpAffine(img_copy, matrix, (width, height))
        return img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.base_img_path)
        if self.__gui:
            print('Proc : PhaseCorrelate_XY')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     img = cv2.imread('./0000_img/ECU/ECUlow_2.jpg')
#     # img = cv2.imread('./0000_img/ECU/rotate2.jpg')
#     param = ['./0000_img/ECU/ECUlow_base.jpg']
#     # param = []
#     app = PhaseCorrelateXY(img, param, gui=True)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./PhaseCorrelate_XY.jpg', dst_img)
