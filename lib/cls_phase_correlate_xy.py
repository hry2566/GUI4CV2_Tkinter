import os
import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class PhaseCorrelate_XY(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.base_img_path = ''
        self.__proc_flag = False

        if len(param) == 1:
            self.base_img_path = param[0]
            pass
        else:
            pass

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__phase_correlate_xy()

        if gui:
            self.Draw()
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
        pass

    def __open_file(self):
        root = tk.Tk()
        root.withdraw()
        typ = [('', '*')]
        dir = './'
        file = filedialog.askopenfilenames(
            filetypes=typ, initialdir=dir)
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

        if not path == '':
            self.base_img_path = path
            self.entry1.delete('0', 'end')
            self.entry1.insert('0', self.base_img_path)
            self.dst_img = self.__phase_correlate_xy()
            self.Draw()
        self.__proc_flag = False
        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
        pass

    def __phase_correlate_xy(self):
        img_copy = self.origin_img.copy()
        img_copy_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        img_copy_float = np.float32(img_copy_gray)

        if self.base_img_path == '':
            img = img_copy
        else:
            h, w, ch = img_copy.shape
            base_img = cv2.imread(self.base_img_path)
            base_img = cv2.cvtColor(base_img, cv2.COLOR_BGR2GRAY)
            base_img_float = np.float32(base_img)
            d, _ = cv2.phaseCorrelate(img_copy_float, base_img_float)
            dx, dy = d
            M = np.float32([[1, 0, dx], [0, 1, dy]])
            img = cv2.warpAffine(img_copy, M, (w, h))
        return img

    def get_data(self):
        param = []
        param.append(self.base_img_path)
        print('Proc : PhaseCorrelate_XY')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/ECU/ECUlow_2.jpg')
    # img = cv2.imread('./0000_img/ECU/rotate2.jpg')
    param = ['./0000_img/ECU/ECUlow_base.jpg']
    # param = []
    app = PhaseCorrelate_XY(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./PhaseCorrelate_XY.jpg', dst_img)
