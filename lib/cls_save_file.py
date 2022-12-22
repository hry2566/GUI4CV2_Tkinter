"""ファイルを開く"""
import os
import tkinter
from tkinter import filedialog

import cv2


class SaveFile():
    """ファイルを開くクラス"""

    def __init__(self, img, param, master=None, gui=False):
        self.dst_img = img
        self.__file_path = ''
        self.__gui = gui

        if len(param) == 1:
            self.__file_path = param[0]

        if gui:
            self.__file_path = self.__save_file()

        if not self.__file_path == '':
            img = self.__imwrite(self.__file_path, self.dst_img)

    def __save_file(self):
        root = tkinter.Tk()
        root.withdraw()
        directory = './'
        file = filedialog.asksaveasfilename(initialdir=directory)
        root.destroy()
        if len(file) == 0:
            path = ''
        else:
            path = file
        return path

    def __imwrite(self, filename, img, params=None):
        try:
            ext = os.path.splitext(filename)[1]
            result, n = cv2.imencode(ext, img, params)

            if result:
                with open(filename, mode='w+b') as file:
                    n.tofile(file)
                return True
            return False
        except Exception as error:
            print(error)
            return False

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.__file_path)
        if self.__gui:
            print('Proc : Save File')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     img = cv2.imread('./0000_img/opencv_logo.jpg')
#     param = []
#     param = ['./save.jpg']
#     app = SaveFile(img, param, gui=True)
