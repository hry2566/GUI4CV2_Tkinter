import tkinter as tk

import cv2

from lib.cls_create_img_memory import Create_Img_Memory
from lib.cls_open_file import OpenFile
from lib.gui.cls_edit_window import EditWindow


class MemoryIO(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.img_bk = img
        self.__img_array_buf2 = []
        self.__img_names_buf2 = []
        self.__memIO = []
        self.__gui=gui

        if type(self.img_bk) == list:
            img = self.img_bk[0]

        if len(param) == 3:
            self.__img_array_buf2 = param[0]
            self.__img_names_buf2 = param[1]
            self.__memIO = param[2]
            pass
        else:
            exit()

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()
        else:
           self.img_bk = self.__memory_io()

        if gui:
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.frame1 = tk.Frame(self.settings_frame)
        self.frame3 = tk.Frame(self.frame1)
        self.frame6 = tk.Frame(self.frame3)
        self.__tkvar = tk.StringVar(value='source_IMG')
        __values = []
        for name in self.__img_names_buf2:
            __values.append(name)
        self.optionmenu1 = tk.OptionMenu(
            self.frame6, self.__tkvar, self.__tkvar.get(), *__values, command=self.__onSelectedMenu)
        self.optionmenu1.pack(fill='x', side='top')
        self.listbox1 = tk.Listbox(self.frame6)
        self.listbox1.pack(expand='true', fill='both', side='top')
        self.frame6.configure(height='200', width='200')
        self.frame6.pack(expand='true', fill='both', side='left')
        self.frame7 = tk.Frame(self.frame3)
        self.button2 = tk.Button(self.frame7)
        self.button2.configure(text='add', command=self.__onBtn2Click)
        self.button2.pack(fill='x', side='top')
        self.button3 = tk.Button(self.frame7)
        self.button3.configure(text='del', command=self.__onBtn3Click)
        self.button3.pack(fill='x', side='top')
        self.frame7.configure(height='200', width='200')
        self.frame7.pack(side='left')
        self.frame9 = tk.Frame(self.frame3)
        self.label1 = tk.Label(self.frame9)
        self.label1.pack(pady='5', side='top')
        self.listbox2 = tk.Listbox(self.frame9)
        self.listbox2.pack(expand='true', fill='both', side='top')
        self.frame9.configure(height='200', width='200')
        self.frame9.pack(expand='true', fill='both', side='left')
        self.frame3.configure(height='200', width='200')
        self.frame3.pack(expand='true', fill='both', side='top')
        self.frame1.configure(height='200', width='200')
        self.frame1.pack(expand='true', fill='both', side='top')
        self.frame2 = tk.Frame(self.settings_frame)
        self.button1 = tk.Button(self.frame2)
        self.button1.configure(text='exec', command=self.__onBtn1Click)
        self.button1.pack(fill='x', side='top')
        self.frame2.configure(height='200', width='200')
        self.frame2.pack(fill='x', side='top')

        if type(self.img_bk) == list:
            for cnt, _ in enumerate(self.img_bk):
                self.listbox2.insert(tk.END, f'source_IMG[{cnt}]')
        else:
            self.listbox2.insert(tk.END, 'source_IMG')

        for name in self.__img_names_buf2:
            self.listbox2.insert(tk.END, name)

        # self.listbox2.select_set(0)

        if not len(self.__memIO) == 0:
            if self.__memIO[0] == '':
                self.__tkvar.set('source_IMG')
                self.__memIO[0] = 'source_IMG'
            else:
                self.__tkvar.set(self.__memIO[0])

            for name in self.__memIO[1]:
                self.listbox1.insert(tk.END, name)

    def __init_events(self):
        self.listbox2.bind('<<ListboxSelect>>', self.__onLst2Select)
        pass

    def __onScale(self, events):
        pass

    def __onSelectedMenu(self, event):
        self.__memIO[0] = self.__tkvar.get()

        while(True):
            if self.listbox1.get(0) == '':
                break
            self.listbox1.delete(0)
        pass

    def __onBtn1Click(self):
        self.img_bk = self.__memory_io()
        pass

    def __onBtn2Click(self):
        if self.listbox2.curselection() == ():
            return

        input_name = self.__tkvar.get()
        if not input_name.startswith('source_IMG'):
            index = self.listbox2.curselection()[0]
            name = self.listbox2.get(index)
            if self.listbox1.get(0) == '' and name.startswith('source_IMG'):
                self.__addLst1()
        else:
            self.__addLst1()
        pass

    def __addLst1(self):
        index = self.listbox2.curselection()[0]
        name = self.listbox2.get(index)
        flag = False
        for index in range(10000):
            lst1_name = self.listbox1.get(index)
            if lst1_name == '':
                break
            if lst1_name == name:
                flag = True
                break

        if not flag:
            self.listbox1.insert(tk.END, name)
            self.__memIO[1].append(name)
        pass

    def __onBtn3Click(self):
        if self.listbox1.curselection() == ():
            return

        index = self.listbox1.curselection()[0]
        self.listbox1.delete(index)
        self.__memIO[1].pop(index)
        pass

    def __onLst2Select(self, event):
        if self.listbox2.curselection() == ():
            return

        index = self.listbox2.curselection()[0]
        name = self.listbox2.get(index)
        
        if name.startswith('source_IMG['):
            name_index = int(name.replace('source_IMG[', '').replace(']', ''))
            self.dst_img = self.img_bk[name_index]
        else:
            if name.startswith('source_IMG'):
                self.dst_img = self.img_bk
            else:
                name_index = self.__img_names_buf2.index(name)
                self.dst_img = self.__img_array_buf2[name_index]
                # cv2.imwrite(f'{name}.png',self.dst_img)
        self.Draw()
        pass

    def __memory_io(self):
        img = self.img_bk.copy()
        target_name = self.__memIO[0]
        set_name_array = self.__memIO[1]

        if target_name == 'source_IMG':
            img = []
            for set_name in set_name_array:
                if set_name.startswith('source_IMG['):
                    set_index = int(set_name.replace('source_IMG[', '').replace(']', ''))
                    img.append(self.img_bk[set_index])
                elif set_name== 'source_IMG':
                    img.append(self.img_bk)
                else:
                    set_index = self.__img_names_buf2.index(set_name)
                    img.append(self.__img_array_buf2[set_index])
        else:
            set_name = self.__memIO[1][0]
            if set_name.startswith('source_IMG['):
                set_index = int(set_name.replace('source_IMG[', '').replace(']', ''))
                targer_index = self.__img_names_buf2.index(target_name)
                self.__img_array_buf2[targer_index] = self.img_bk[set_index]
            else:
                self.__img_array_buf2[self.__img_names_buf2.index(target_name)]=self.img_bk

        if type(img) == list:
            if len(img) == 1:
                img = img[0]

        return img

    def get_data(self):
        param = []
        param = [self.__img_array_buf2, self.__img_names_buf2,self.__memIO]
        if self.__gui:
            print('Proc : MemoryIO')
            print(f'param = {param[2]}')
        return param, self.img_bk


if __name__ == "__main__":
    param = ['C:/Users/2566haraya/Desktop/GitHub/OpenCV-GUI/0000_img/opencv_logo2.jpg']
    imgLib = OpenFile(param, gui=False)
    param, img = imgLib.get_data()

    img_array = []
    img_names = ['img1', 'img2']
    param = [img_array, img_names]
    imgLib = Create_Img_Memory(img, [img_array, img_names], gui=False)
    param, img = imgLib.get_data()
    img_array = param[0]
    img_names = param[1]

    dummy1 = cv2.imread('C:/Users/2566haraya/Desktop/GitHub/OpenCV-GUI/0000_img/opencv_logo.jpg')
    dummy2 = img
    
    img=[]
    img.append(dummy1)
    img.append(dummy2)
    img_array[0]=dummy2
    img_array[1]=dummy1

    # memIO = ['img1', ['source_IMG']]
    # memIO = ['img1', ['source_IMG[0]']]
    memIO = ['img1', ['source_IMG[1]']]
    param = [img_array, img_names, memIO]
    imgLib = MemoryIO(img, param, gui=True)
    param, img = imgLib.get_data()
    img_array = param[0]

    # cv2.imwrite('./MemoryIO10.jpg', img[0])
    # cv2.imwrite('./MemoryIO20.jpg', img[1])
    # cv2.imwrite('./MemoryIO10.jpg', img)
    cv2.imwrite('./MemoryIO10.jpg', img[0])
    cv2.imwrite('./MemoryIO20.jpg', img[1])
    cv2.imwrite('./MemoryIO30.jpg', img_array[0])
    cv2.imwrite('./MemoryIO40.jpg', img_array[1])

    