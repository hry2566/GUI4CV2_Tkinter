import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class Create_Img_Memory(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = np.zeros((1, 1, 3), np.uint8)
        self.through_img = img
        self.__img_array = []
        self.__img_names = []
        # self.__proc_flag = False

        if len(param) == 2:
            self.__img_names = param[1]
            for i in param[1]:
                self.__img_array.append(self.origin_img)
        else:
            exit()

        if gui:
            super().__init__(self.origin_img, master)
            self.__init_gui()
            self.__init_events()
            if len(param) == 2:
                for i in param[1]:
                    self.listbox1.insert(tk.END, i)
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.frame1 = tk.Frame(self.settings_frame)
        self.frame3 = tk.Frame(self.frame1)
        self.label1 = tk.Label(self.frame3)
        self.label1.configure(text='img name')
        self.label1.pack(anchor='w', side='top')
        self.entry2 = tk.Entry(self.frame3)
        self.entry2.configure(width='15')
        _text_ = '''img1'''
        self.entry2.delete('0', 'end')
        self.entry2.insert('0', _text_)
        self.entry2.pack(side='top')
        self.frame3.configure(height='200', width='200')
        self.frame3.pack(pady='5', side='left')
        self.button1 = tk.Button(self.frame1)
        self.button1.configure(text='add')
        self.button1.pack(anchor='s', side='left')
        self.button2 = tk.Button(self.frame1)
        self.button2.configure(text='del')
        self.button2.pack(anchor='s', side='left')
        self.frame1.configure(height='200', width='200')
        self.frame1.pack(fill='x', padx='5', pady='5', side='top')
        self.frame2 = tk.Frame(self.settings_frame)
        self.listbox1 = tk.Listbox(self.frame2)
        self.listbox1.pack(expand='true', fill='both', side='top')
        self.frame2.configure(height='200', width='200')
        self.frame2.pack(expand='true', fill='both',
                         padx='5', pady='5', side='top')

        self.settings_frame.pack(expand='true', fill='both', side='top')

        self.image_view_frame.pack_forget()
        pass

    def __init_events(self):
        self.button1.bind('<1>', self.__onAddBtn)
        self.button2.bind('<1>', self.__onDelBtn)
        self.entry2.bind('<Return>', self.__onReturn)
        pass

    def __onReturn(self, event):
        self.__onAddBtn(None)

    def __onAddBtn(self, event):
        add_name = self.entry2.get()
        index = 0
        flag = False
        while(True):
            if self.listbox1.get(index) == '':
                break
            if self.listbox1.get(index) == add_name:
                flag = True
            index += 1
        if not flag:
            self.listbox1.insert(tk.END, add_name)
            self.__img_array.append(self.origin_img)
            self.__img_names.append(add_name)
        pass

    def __onDelBtn(self, event):
        if not self.listbox1.curselection() == ():
            select_index = self.listbox1.curselection()[0]
            self.__img_array.pop(select_index)
            self.__img_names.pop(select_index)
            self.listbox1.delete(select_index)
        pass

    def get_data(self):
        param = []
        param.append(self.__img_array)
        param.append(self.__img_names)
        print('Proc : Create IMG Memory')
        print(f'len(img_array) = {len(self.__img_array)}')
        print(f'img_names = {param[1]}')
        print('param = [img_array, img_names]')
        return param, self.through_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    img_array = []
    img_names = ['img1', 'img2']
    app = Create_Img_Memory(img, [img_array, img_names], gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./Create_Img_Memory.jpg', dst_img)
