import tkinter
from tkinter import filedialog

import cv2


class SaveFile():
    def __init__(self, img, param, master=None, gui=False):
        self.dst_img = img
        self.__file_path = ''

        if len(param) == 1:
            self.__file_path = param[0]

        if gui:
            self.__file_path = self.__save_file()

        if not self.__file_path == '':
            img = cv2.imwrite(self.__file_path, self.dst_img)

    def __save_file(self):
        root = tkinter.Tk()
        root.withdraw()
        dir = './'
        file = filedialog.asksaveasfilename(initialdir=dir)
        root.destroy()
        if len(file) == 0:
            path = ''
        else:
            path = file
        return path

    def get_data(self):
        param = []
        param.append(self.__file_path)
        print('Proc : Save File')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    param = ['./save.jpg']
    app = SaveFile(img, param, gui=True)
