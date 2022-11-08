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
                # 日本語ファイル／パス対応
                img = self.__imread(self.__file_path)

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

    def __imread(self, filename, flags=cv2.IMREAD_COLOR, dtype=np.uint8):
        try:
            n = np.fromfile(filename, dtype)
            img = cv2.imdecode(n, flags)
            return img
        except Exception as e:
            print(e)
            return None

    def __imwrite(self, filename, img, params=None):
        try:
            ext = os.path.splitext(filename)[1]
            result, n = cv2.imencode(ext, img, params)

            if result:
                with open(filename, mode='w+b') as f:
                    n.tofile(f)
                return True
            else:
                return False
        except Exception as e:
            print(e)
            return False

    def get_data(self):
        param = []
        img=[]
        param.append(self.__file_path)
        if self.__file_path == '':
            self.dst_img = []
        else:
            # 日本語ファイル／パス対応
            img = self.__imread(self.__file_path)

        print('Proc : Open File')
        print(f'param = {param}')
        return param, img


if __name__ == "__main__":
    param = []
    # param = ['./0000_img/opencv_logo.jpg']
    # param = ['./0000_img/opencv_logo.jpg']
    app = OpenFile(param, gui=True)
    param, dst_img = app.get_data()
    # cv2.imwrite('./open.jpg', dst_img)
