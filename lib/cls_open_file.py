import tkinter as tk
import tkinter
import cv2
from tkinter import filedialog
from lib.gui.cls_edit_window import EditWindow


class OpenFile(EditWindow):
    def __init__(self, param, master=None, gui=False):
        self.dst_img = None

        if len(param) == 1:
            self.__file_path = param[0]
        else:
            self.__file_path = ''

        if gui:
            self.__file_path = self.__open_file()
            if not self.__file_path == '':
                img = cv2.imread(self.__file_path)
                super().__init__(img, master)
                if master == None:
                    self.__init_gui()

        if gui and not self.__file_path == '':
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
        file = filedialog.askopenfilenames(filetypes=typ, initialdir=dir)
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
            self.dst_img = None
        else:
            self.dst_img = cv2.imread(self.__file_path)

        print('Proc : Open File')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    param = []
    param = ['./0000_img/opencv_logo.jpg']
    app = OpenFile(param, gui=True)
    param, dst_img = app.get_data()
