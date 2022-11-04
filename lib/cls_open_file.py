import os
import tkinter
from tkinter import filedialog

import cv2
import numpy as np
from PIL import Image

from lib.gui.cls_edit_window import EditWindow


class OpenFile(EditWindow):
    def __init__(self, param, master=None, gui=False):
        self.dst_img = []
        self.__file_path = ''

        if len(param) == 1:
            self.__file_path = param[0]

        if gui:
            self.__file_path = self.__open_file()
            if not self.__file_path == '':
                # img = cv2.imread(self.__file_path)

                # 日本語ファイル／パス対応
                pil_img = Image.open(self.__file_path)
                img = np.array(pil_img)
                if img.ndim == 3:
                    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                cv2.imwrite('dummy.jpg', img)
                img = cv2.imread('dummy.jpg')
                os.remove('./dummy.jpg')

                super().__init__(img, master)
                if master == None:
                    self.__init_gui()
                self.run()

    def __init_gui(self):
        self.none_label.destroy()
        self.mainwindow.title('Open File')
        pass

    def __open_file(self):
        root = tkinter.Tk()
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
        return path

    def get_data(self):
        param = []
        param.append(self.__file_path)
        if self.__file_path == '':
            self.dst_img = []
        else:
            # self.dst_img = cv2.imread(self.__file_path)
            # 日本語ファイル／パス対応
            pil_img = Image.open(self.__file_path)
            img = np.array(pil_img)
            if img.ndim == 3:
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
            cv2.imwrite('dummy.jpg', img)
            self.dst_img = cv2.imread('dummy.jpg')
            os.remove('./dummy.jpg')


        print('Proc : Open File')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    param = []
    # param = ['./0000_img/opencv_logo.jpg']
    # param = ['./0000_img/opencv_logo.jpg']
    app = OpenFile(param, gui=True)
    param, dst_img = app.get_data()
    # cv2.imwrite('./open.jpg', dst_img)
