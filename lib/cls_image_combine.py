import tkinter as tk

import cv2

from lib.gui.cls_edit_window import EditWindow


class ImageCombine(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.img_bk = img
        self.__radio_index = 0

        if not type(img) == list:
            self.dst_img = img
            return

        self.origin_img = cv2.hconcat(img)
        # self.__proc_flag = False

        if len(param) == 1:
            self.__radio_index = param[0]

        if gui:
            super().__init__(self.origin_img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__image_combine()

        if gui:
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.radio_var = tk.IntVar()
        self.radio_var.set(self.__radio_index)
        val1 = 0
        val2 = 1
        self.radiobutton1 = tk.Radiobutton(
            self.settings_frame, value=val1, variable=self.radio_var)
        self.radiobutton1.configure(
            text='horizontal', command=self.__radioClick)
        self.radiobutton1.pack(side='top', anchor='w')
        self.radiobutton2 = tk.Radiobutton(
            self.settings_frame, value=val2, variable=self.radio_var)
        self.radiobutton2.configure(
            text='virtical', command=self.__radioClick)
        self.radiobutton2.pack(side='top',  anchor='w')
        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
        pass

    def __radioClick(self):
        self.__radio_index = self.radio_var.get()
        self.dst_img = self.__image_combine()
        self.Draw()

    def __image_combine(self):
        img_copy = self.img_bk.copy()
        if self.__radio_index == 0:
            img = cv2.hconcat(img_copy)
        else:
            img = cv2.vconcat(img_copy)
        return img

    def get_data(self):
        param = []
        param.append(self.__radio_index)
        print('Proc : ImageCombine')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img1 = cv2.imread('./0000_img/opencv_logo.jpg')
    img2 = cv2.imread('./0000_img/opencv_logo2.jpg')
    # img3 = cv2.imread('./0000_img/opencv_logo2.jpg')
    img = []
    img.append(img1)
    img.append(img2)
    # img.append(img3)
    param = [0]
    # img = cv2.imread('./0000_img/opencv_logo.jpg')
    app = ImageCombine(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./ImageCombine.jpg', dst_img)
