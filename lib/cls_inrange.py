import tkinter as tk

import cv2

from lib.gui.cls_edit_window import EditWindow


class InRange(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__proc_flag = False

        if len(param) == 6:
            self.__r_h_1 = param[0]
            self.__g_s_1 = param[1]
            self.__b_v_1 = param[2]
            self.__r_h_2 = param[3]
            self.__g_s_2 = param[4]
            self.__b_v_2 = param[5]
        else:
            self.__r_h_1 = 0
            self.__g_s_1 = 0
            self.__b_v_1 = 0
            self.__r_h_2 = 255
            self.__g_s_2 = 255
            self.__b_v_2 = 255

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__inrange()

        if gui:
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = tk.Scale(self.settings_frame)
        self.__scale1.configure(from_=0, to=255,
                                label='r(v)_1', orient="horizontal", command=self.__onScale)
        self.__scale1.pack(side="top")

        self.__scale2 = tk.Scale(self.settings_frame)
        self.__scale2.configure(from_=0, to=255,
                                label='g(s)_1', orient="horizontal", command=self.__onScale)
        self.__scale2.pack(side="top")

        self.__scale3 = tk.Scale(self.settings_frame)
        self.__scale3.configure(from_=0, to=255,
                                label='b(h)_1', orient="horizontal", command=self.__onScale)
        self.__scale3.pack(side="top")

        self.__scale4 = tk.Scale(self.settings_frame)
        self.__scale4.configure(from_=0, to=255,
                                label='r(v)_2', orient="horizontal", command=self.__onScale)
        self.__scale4.pack(side="top")

        self.__scale5 = tk.Scale(self.settings_frame)
        self.__scale5.configure(from_=0, to=255,
                                label='g(s)_2', orient="horizontal", command=self.__onScale)
        self.__scale5.pack(side="top")

        self.__scale6 = tk.Scale(self.settings_frame)
        self.__scale6.configure(from_=0, to=255,
                                label='b(h)_2', orient="horizontal", command=self.__onScale)
        self.__scale6.pack(side="top")

        self.__scale1.set(self.__r_h_1)
        self.__scale2.set(self.__g_s_1)
        self.__scale3.set(self.__b_v_1)
        self.__scale4.set(self.__r_h_2)
        self.__scale5.set(self.__g_s_2)
        self.__scale6.set(self.__b_v_2)

        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__r_h_1 = self.__scale1.get()
        self.__g_s_1 = self.__scale2.get()
        self.__b_v_1 = self.__scale3.get()
        self.__r_h_2 = self.__scale4.get()
        self.__g_s_2 = self.__scale5.get()
        self.__b_v_2 = self.__scale6.get()

        self.dst_img = self.__inrange()
        self.Draw()
        self.__proc_flag = False
        pass

    def __inrange(self):
        img_copy = self.origin_img.copy()

        img = cv2.inRange(img_copy,
                          (self.__b_v_1, self.__g_s_1, self.__r_h_1),
                          (self.__b_v_2, self.__g_s_2, self.__r_h_2))
        return img

    def get_data(self):
        param = []
        param.append(self.__r_h_1)
        param.append(self.__g_s_1)
        param.append(self.__b_v_1)
        param.append(self.__r_h_2)
        param.append(self.__g_s_2)
        param.append(self.__b_v_2)
        img = cv2.cvtColor(self.dst_img, cv2.COLOR_GRAY2BGR)
        print('Proc : inRange')
        print(f'param = {param}')
        return param, img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    param = [33, 33, 3]
    app = InRange(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./inrange.jpg', dst_img)
