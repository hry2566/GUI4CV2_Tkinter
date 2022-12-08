import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class Edge_Arc(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__center_x = int(img.shape[1]/2)
        self.__center_y = int(img.shape[0]/2)
        self.__radius = 0
        self.__length = 0
        self.__thresh1 = 1
        self.__kernel = 0
        self.__gain = 0.2
        self.__img_array = [img, img, img, img, img]
        self.__img_array[0] = img
        self.__index = 0
        self.__result = []
        self.__proc_flag = False

        if len(param) == 3:
            self.__center_x = param[0][0][0]
            self.__center_y = param[0][0][1]
            self.__radius = param[0][1]
            self.__length = param[0][2]
            self.__thresh1 = param[1][0]
            self.__kernel = param[1][1]
            self.__gain = param[1][2]
            pass
        else:
            pass

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__edge_arc()

        if gui:
            self.__draw_list()
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.radio_value = tk.IntVar(value=4)

        self.labelframe1 = tk.LabelFrame(self.settings_frame)
        self.labelframe1.configure(height=200, text='view', width=200)
        self.radiobutton1 = tk.Radiobutton(self.labelframe1)
        self.radiobutton1.configure(text='area')
        self.radiobutton1.pack(anchor="w", side="top")
        self.radiobutton2 = tk.Radiobutton(self.labelframe1)
        self.radiobutton2.configure(text='threshold1')
        self.radiobutton2.pack(anchor="w", side="top")
        self.radiobutton3 = tk.Radiobutton(self.labelframe1)
        self.radiobutton3.configure(text='morphology')
        self.radiobutton3.pack(anchor="w", side="top")
        self.radiobutton4 = tk.Radiobutton(self.labelframe1)
        self.radiobutton4.configure(text='laplacian')
        self.radiobutton4.pack(anchor="w", side="top")
        self.labelframe1.pack(fill="x", padx=5, side="top")
        self.labelframe2 = tk.LabelFrame(self.settings_frame)
        self.labelframe2.configure(height=200, text='area', width=200)
        self.scale_x = tk.Scale(self.labelframe2)
        self.scale_x.configure(label='x', orient="horizontal")
        self.scale_x.pack(fill="x", side="top")
        self.scale_y = tk.Scale(self.labelframe2)
        self.scale_y.configure(label='y', orient="horizontal")
        self.scale_y.pack(fill="x", side="top")
        self.scale_radius = tk.Scale(self.labelframe2)
        self.scale_radius.configure(label='radius', orient="horizontal")
        self.scale_radius.pack(fill="x", side="top")
        self.scale_length = tk.Scale(self.labelframe2)
        self.scale_length.configure(label='length', orient="horizontal")
        self.scale_length.pack(fill="x", side="top")
        self.labelframe2.pack(fill="x", padx=5, side="top")
        self.labelframe3 = tk.LabelFrame(self.settings_frame)
        self.labelframe3.configure(height=200, text='threshold1', width=200)
        self.scale_threshold1 = tk.Scale(self.labelframe3)
        self.scale_threshold1.configure(orient="horizontal")
        self.scale_threshold1.pack(fill="x", side="top")
        self.labelframe3.pack(fill="x", padx=5, side="top")
        self.labelframe4 = tk.LabelFrame(self.settings_frame)
        self.labelframe4.configure(height=200, text='morphology', width=200)
        self.scale_morpholory = tk.Scale(self.labelframe4)
        self.scale_morpholory.configure(orient="horizontal")
        self.scale_morpholory.pack(fill="x", side="top")
        self.labelframe4.pack(fill="x", padx=5, side="top")

        self.labelframe8 = tk.LabelFrame(self.settings_frame)
        self.labelframe8.configure(height=200, text='execute', width=200)
        self.label1 = tk.Label(self.labelframe8)
        self.label1.configure(text='gain', width=6)
        self.label1.pack(side="top", anchor='w')
        self.entry1 = tk.Entry(self.labelframe8)
        _text_ = '0'
        self.entry1.delete("0", "end")
        self.entry1.insert("0", _text_)
        self.entry1.pack(fill="x", padx=5, pady=5, side="top")
        self.button1 = tk.Button(self.labelframe8)
        self.button1.configure(text='exec')
        self.button1.pack(fill="x", padx=5, pady=5, side="top")
        self.label2 = tk.Label(self.labelframe8)
        self.label2.configure(text='result', width=6)
        self.label2.pack(side="top", anchor='w')
        self.result_list = tk.Listbox(self.labelframe8)
        self.result_list.configure(width=40)
        self.result_list.pack(
            expand="true",
            fill="both",
            padx=5,
            pady=5,
            side="top")

        self.labelframe8.pack(fill="x", padx=5, side="top")

        self.radiobutton1.configure(variable=self.radio_value,
                                    value=0, command=self.onClick_radio)
        self.radiobutton2.configure(variable=self.radio_value,
                                    value=1, command=self.onClick_radio)
        self.radiobutton3.configure(variable=self.radio_value,
                                    value=2, command=self.onClick_radio)
        self.radiobutton4.configure(variable=self.radio_value,
                                    value=3, command=self.onClick_radio)

        h, w, _ = self.origin_img.shape

        self.scale_x.configure(from_=0, to=w, command=self.__onScale)
        self.scale_y.configure(from_=0, to=h, command=self.__onScale)

        if h > w:
            r = h
        else:
            r = w
        self.scale_radius.configure(from_=0, to=r, command=self.__onScale)
        self.scale_length.configure(from_=0, to=r, command=self.__onScale)

        self.scale_threshold1.configure(from_=0,
                                        to=255,
                                        command=self.__onScale)
        self.scale_morpholory.configure(from_=0,
                                        to=20,
                                        command=self.__onScale)
        self.button1.configure(command=self.__onClick_exec)

        self.__proc_flag = True
        self.scale_x.set(self.__center_x)
        self.scale_y.set(self.__center_y)
        self.scale_radius.set(self.__radius)
        self.scale_length.set(self.__length)
        self.scale_threshold1.set(self.__thresh1)
        self.scale_morpholory.set(self.__kernel)
        self.entry1.delete("0", "end")
        self.entry1.insert("0", self.__gain)

        self.__set_param_view(self.radio_value.get())
        self.__proc_flag = False

    def __init_events(self):
        self.entry1.bind('<Return>', self.__onEnter)
        pass

    def __onEnter(self, event):
        self.__gain = float(self.entry1.get())
        self.dst_img = self.__result_view()
        self.__draw_list()
        self.Draw()

    def __onClick_exec(self):
        self.__gain = float(self.entry1.get())
        self.radio_value.set(4)
        self.__set_param_view(self.radio_value.get())
        self.dst_img = self.__edge_arc()
        self.__draw_list()
        self.Draw()

    def onClick_radio(self):
        self.__index = self.radio_value.get()
        self.__set_param_view(self.__index)
        if self.__index == 0:
            self.dst_img = self.__set_area_param()
        elif self.__index == 1:
            self.dst_img = self.__set_threshold1_param()
        elif self.__index == 2:
            self.__set_threshold1_param()
            self.dst_img = self.__set_morphology_param()
        elif self.__index == 3:
            self.__set_threshold1_param()
            self.__set_morphology_param()
            self.dst_img = self.__set_laplacian_param()
        self.Draw()

    def __onScale(self, events):
        if self.__proc_flag:
            return

        index = self.radio_value.get()
        if index == 0:
            self.__center_x = self.scale_x.get()
            self.__center_y = self.scale_y.get()
            self.__radius = self.scale_radius.get()
            self.__length = self.scale_length.get()
            self.dst_img = self.__set_area_param()
        elif index == 1:
            self.__thresh1 = self.scale_threshold1.get()
            self.dst_img = self.__set_threshold1_param()
        elif index == 2:
            self.__kernel = self.scale_morpholory.get()
            self.dst_img = self.__set_morphology_param()
        elif index == 3:
            self.dst_img = self.__set_laplacian_param()
        self.Draw()

    def __draw_list(self):
        self.result_list.delete(0, tk.END)
        for item in self.__result:
            self.result_list.insert(0, item)

    def __set_param_view(self, index):
        self.__clear_param_view()
        if index == 0:
            self.labelframe2.pack(fill="x", padx=5, side="top")
        elif index == 1:
            self.labelframe3.pack(fill="x", padx=5, side="top")
        elif index == 2:
            self.labelframe4.pack(fill="x", padx=5, side="top")
        elif index == 3:
            pass
        self.labelframe8.pack(fill="x", padx=5, side="top")
        self.button1.pack(fill="x", padx=5, pady=5, side="top")

    def __clear_param_view(self):
        self.labelframe2.pack_forget()
        self.labelframe3.pack_forget()
        self.labelframe4.pack_forget()
        self.labelframe8.pack_forget()

    def __result_view(self):
        img_copy = self.__img_array[0].copy()

        rect1_x1 = self.__center_x+self.__radius
        rect1_y1 = self.__center_y
        rect1_x2 = self.__center_x+self.__radius+self.__length
        rect1_y2 = self.__center_y+1

        rect2_x1 = self.__center_x
        rect2_y1 = self.__center_y-(self.__radius+self.__length)
        rect2_x2 = self.__center_x+1
        rect2_y2 = self.__center_y-self.__radius

        rect3_x1 = self.__center_x-(self.__radius+self.__length)
        rect3_y1 = self.__center_y
        rect3_x2 = self.__center_x-self.__radius
        rect3_y2 = self.__center_y+1

        rect4_x1 = self.__center_x
        rect4_y1 = self.__center_y+self.__radius
        rect4_x2 = self.__center_x+1
        rect4_y2 = self.__center_y+(self.__radius+self.__length)

        center = (self.__center_x, self.__center_y)

        img_rotate = self.__img_array[3].copy()
        width, height = self.__img_array[3].shape

        self.__result = []
        for cnt in range(89):
            trans = cv2.getRotationMatrix2D(center, cnt, 1)
            img_rotate = cv2.warpAffine(
                self.__img_array[3].copy(), trans, (width, height))

            area1 = img_rotate[rect1_y1: rect1_y2, rect1_x1: rect1_x2]
            white_area1 = cv2.countNonZero(area1)
            area2 = img_rotate[rect2_y1: rect2_y2, rect2_x1: rect2_x2]
            white_area2 = cv2.countNonZero(area2)
            area3 = img_rotate[rect3_y1: rect3_y2, rect3_x1: rect3_x2]
            white_area3 = cv2.countNonZero(area3)
            area4 = img_rotate[rect4_y1: rect4_y2, rect4_x1: rect4_x2]
            white_area4 = cv2.countNonZero(area4)

            if white_area1 > area1.shape[0]*area1.shape[1]*self.__gain:
                start_x, start_y = center
                length = self.__radius+self.__length
                img_copy = cv2.ellipse(img_copy, (start_x, start_y), (length, 0),
                                       cnt, 0, 90, color=(0, 0, 255), thickness=-1)
                self.__result.append(abs(cnt))
            if white_area2 > area2.shape[0]*area2.shape[1]*self.__gain:
                start_x, start_y = center
                length = self.__radius+self.__length
                img_copy = cv2.ellipse(img_copy, (start_x, start_y), (length, 0),
                                       cnt-90, 0, 90, color=(0, 0, 255), thickness=-1)
                self.__result.append(abs(cnt-90))
            if white_area3 > area3.shape[0]*area3.shape[1]*self.__gain:
                start_x, start_y = center
                length = self.__radius+self.__length
                img_copy = cv2.ellipse(img_copy, (start_x, start_y), (length, 0),
                                       cnt-180, 0, 90, color=(0, 0, 255), thickness=-1)
                self.__result.append(abs(cnt-180))
            if white_area4 > area4.shape[0]*area4.shape[1]*self.__gain:
                start_x, start_y = center
                length = self.__radius+self.__length
                img_copy = cv2.ellipse(img_copy, (start_x, start_y), (length, 0),
                                       cnt-270, 0, 90, color=(0, 0, 255), thickness=-1)
                self.__result.append(abs(cnt-270))

        self.__img_array[4] = img_copy
        return img_copy

    def __set_laplacian_param(self):
        img_gray = self.__img_array[2].copy()
        img_gray = cv2.Laplacian(
            img_gray.copy(), cv2.CV_64F, ksize=3).astype(np.uint8)
        self.__img_array[3] = img_gray
        return img_gray

    def __set_morphology_param(self):
        img_gray = self.__img_array[1].copy()
        kernel = np.ones((self.__kernel, self.__kernel), np.uint8)
        img_gray = cv2.morphologyEx(img_gray, cv2.MORPH_CLOSE, kernel)
        img_gray = cv2.morphologyEx(img_gray, cv2.MORPH_OPEN, kernel)
        self.__img_array[2] = img_gray
        return img_gray

    def __set_threshold1_param(self):
        img_gray = cv2.cvtColor(self.origin_img.copy(), cv2.COLOR_BGR2GRAY)
        _, img_gray = cv2.threshold(img_gray,
                                    self.__thresh1,
                                    255,
                                    cv2.THRESH_BINARY)
        self.__img_array[1] = img_gray
        return img_gray

    def __set_area_param(self):
        if self.__proc_flag:
            return self.__img_array[0]

        center = (self.__center_x, self.__center_y)
        img_copy = self.origin_img.copy()
        cv2.circle(img_copy, center, self.__radius, (0, 255, 0), 3)
        cv2.circle(img_copy, center, self.__radius +
                   self.__length, (0, 255, 0), 3)
        self.__img_array[0] = img_copy
        return self.__img_array[0]

    def __edge_arc(self):
        img_copy = self.origin_img.copy()
        self.__set_area_param()
        self.__set_threshold1_param()
        self.__set_morphology_param()
        self.__set_laplacian_param()
        img_copy = self.__result_view()
        return img_copy

    def get_data(self):
        param = []
        param.append([(self.__center_x, self.__center_y),
                     self.__radius, self.__length])
        param.append([self.__thresh1, self.__kernel, self.__gain])
        param.append(self.__result)
        print('Proc : Edge_Arc')
        print(f'param = {param}')
        return param, self.__result_view()


if __name__ == "__main__":
    img = cv2.imread('./0000_img/bush/b1.jpg')
    param = []
    # param = [[(1215, 1037), 320, 54], [239, 7, 0.5], [173, 170]]
    app = Edge_Arc(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./Edge_Arc.jpg', dst_img)
