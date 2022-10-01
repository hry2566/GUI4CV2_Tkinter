import tkinter as tk

import cv2

from lib.gui.cls_edit_window import EditWindow, even2odd


class Adaptive_Thresholed(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__proc_flag = False
        self.__adaptiveMethod = [cv2.ADAPTIVE_THRESH_MEAN_C,
                                 cv2.ADAPTIVE_THRESH_GAUSSIAN_C]

        if len(param) == 4:
            self.__method_index = param[0]
            self.__Value = param[1]
            self.__block_size = param[2]
            self.__c = param[3]
        else:
            self.__method_index = 0
            self.__Value = 255
            self.__block_size = 3
            self.__c = 1

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__adaptive_thresholed()

        if gui:
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__tkvar = tk.StringVar(value='MEAN')
        __values = ['MEAN', 'GAUSSIAN']
        self.__optionmenu2 = tk.OptionMenu(
            self.settings_frame, self.__tkvar, *__values, command=self.__onSelect)
        self.__optionmenu2.pack(fill='x', side='top')

        self.__scale1 = tk.Scale(self.settings_frame)
        self.__scale1.configure(from_=0, to=255,
                                label='Value', orient='horizontal', command=self.__onScale)
        self.__scale1.pack(side='top')
        self.__scale2 = tk.Scale(self.settings_frame)
        self.__scale2.configure(from_=3, to=255,
                                label='block_size', orient='horizontal', command=self.__onScale)
        self.__scale2.pack(side='top')
        self.__scale3 = tk.Scale(self.settings_frame)
        self.__scale3.configure(from_=1, to=255,
                                label='c', orient='horizontal', command=self.__onScale)
        self.__scale3.pack(side='top')

        self.__scale1.set(self.__Value)
        self.__scale2.set(self.__block_size)
        self.__scale3.set(self.__c)
        pass

    def __init_events(self):
        pass

    def __onSelect(self, event):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        if self.__tkvar.get() == 'MEAN':
            self.__method_index = 0
        elif self.__tkvar.get() == 'GAUSSIAN':
            self.__method_index = 1

        self.dst_img = self.__adaptive_thresholed()
        self.Draw()
        self.__proc_flag = False

    def __onScale(self, events):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__Value = self.__scale1.get()
        self.__block_size = self.__scale2.get()
        self.__c = self.__scale3.get()
        self.dst_img = self.__adaptive_thresholed()
        self.Draw()
        self.__proc_flag = False
        pass

    def __adaptive_thresholed(self):
        img_copy = self.origin_img.copy()
        img_copy = cv2.medianBlur(img_copy, 5)
        img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

        # if int(self.__block_size) % 2 == 0:
        #     self.__block_size += 1

        self.__block_size = even2odd(self.__block_size)

        img = cv2.adaptiveThreshold(img_copy,
                                    self.__Value,
                                    self.__adaptiveMethod[self.__method_index],
                                    cv2.THRESH_BINARY,
                                    self.__block_size,
                                    self.__c)
        return img

    def get_data(self):
        param = []
        param.append(self.__method_index)
        param.append(self.__Value)
        param.append(self.__block_size)
        param.append(self.__c)
        img = cv2.cvtColor(self.dst_img, cv2.COLOR_GRAY2BGR)
        print('Proc : Average')
        print(f'param = {param}')
        return param, img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    param = [0, 255, 3, 1]
    app = Adaptive_Thresholed(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./adaptive_thresholed.jpg', dst_img)
