import os
import tkinter as tk
from tkinter import filedialog

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class PhaseCorrelate(EditWindow):
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

        self.dst_img = self.__phase_correlate()

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
            self.dst_img = self.__phase_correlate()
            self.Draw()
        self.__proc_flag = False
        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
        pass

    def __ripoc(self, a, b, m=None):
        g_a = np.asarray(cv2.cvtColor(a, cv2.COLOR_BGR2GRAY), 'float')
        g_b = np.asarray(cv2.cvtColor(b, cv2.COLOR_BGR2GRAY), 'float')

        h, w = g_a.shape
        hy = np.hanning(h)
        hx = np.hanning(w)
        hw = hy.reshape(h, 1)*hx

        f_a = np.fft.fftshift(np.log(np.abs(np.fft.fft2(g_a*hw))))
        f_b = np.fft.fftshift(np.log(np.abs(np.fft.fft2(g_b*hw))))

        if not m:
            l = np.sqrt(w*w + h*h)
            m = l/np.log(l)

        center = (w/2, h/2)
        flags = cv2.INTER_LANCZOS4 + cv2.WARP_POLAR_LOG
        p_a = cv2.warpPolar(f_a, (w, h), center, m, flags)
        p_b = cv2.warpPolar(f_b, (w, h), center, m, flags)
        (x, y), e = cv2.phaseCorrelate(p_a, p_b, hw)

        angle = y*360/h
        scale = (np.e)**(x/m)
        M = cv2.getRotationMatrix2D(center, angle, scale)
        t_b = cv2.warpAffine((g_b), M, (w, h))
        (x, y), e = cv2.phaseCorrelate(g_a, t_b)
        return x, y, angle, scale

    def __phase_correlate(self):
        img_copy = self.origin_img.copy()

        if self.base_img_path == '':
            img = img_copy
        else:
            base_img = cv2.imread(self.base_img_path)
            x, y, angle, scale = self.__ripoc(base_img, img_copy)
            scale = 1.0
            # print(x, y, angle, scale)
            h, w, ch = img_copy.shape

            M = cv2.getRotationMatrix2D((w/2, h/2), angle, scale)
            M[0][2] -= x
            M[1][2] -= y

            img = cv2.warpAffine(img_copy, M, (w, h))
        return img

    def get_data(self):
        param = []
        param.append(self.base_img_path)
        print('Proc : PhaseCorrelate')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/ECU/ECUlow_2.jpg')
    # img = cv2.imread('./0000_img/ECU/rotate2.jpg')
    param = ['./0000_img/ECU/ECUlow_base.jpg']
    # param = []
    app = PhaseCorrelate(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./PhaseCorrelate.jpg', dst_img)
