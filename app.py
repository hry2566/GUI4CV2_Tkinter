import tkinter as tk
from lib.cls_open_file import OpenFile
from lib.app.cls_app_base import App_Base
from lib.cls_average import Average
from lib.cls_save_file import SaveFile


class App(App_Base):
    def __init__(self, master=None):
        super().__init__(master)
        self.app_child = None
        self.menu_list = []
        self.proc_list = []
        self.param_list = []
        self.dstimg_list = []

        self.__init_gui()
        self.__init_events()

        # img = cv2.imread('./0000_img/opencv_logo.jpg')
        # param = []
        # param = [15, 15]
        # self.dummy_frame.destroy()
        # self.app_child = Average(img, param, master=self.appwindow, gui=True)
        # param, dst_img = self.app_child.get_data()

        # param = []
        # param = ['./0000_img/opencv_logo.jpg']
        # self.dummy_frame.destroy()
        # self.app_child = OpenFile(param, master=self.appwindow, gui=True)
        # param, dst_img = self.app_child.get_data()

        # img = cv2.imread('./0000_img/opencv_logo.jpg')
        # param = []
        # param = ['./save.jpg']
        # self.app_child = SaveFile(img, param, gui=False)

        pass

    def __init_gui(self):
        self.optionmenu1["menu"].delete(0, "last")
        self.menu_list.append('ファイル開く(Open File)')
        self.menu_list.append('ファイル保存(Save File)')
        self.menu_list.append('ぼかし (Average)')

    def __init_events(self):
        for menu in self.menu_list:
            self.optionmenu1["menu"].add_command(
                label=menu, command=tk._setit(self.tkvar, menu))

        self.add_btn.bind('<1>', self.__onAddBtn_Events)
        self.task_list.bind("<<ListboxSelect>>", self.__onSelectListBox_Events)

    def __onAddBtn_Events(self, event):
        task = self.tkvar.get()
        self.task_list.insert(tk.END, task)
        self.proc_list.append(task)
        self.param_list.append([])
        self.dstimg_list.append(None)
        pass

    def __onSelectListBox_Events(self, event):
        index = event.widget.curselection()
        self.__run_proc(event.widget.get(index), index[0])
        pass

    def __run_proc(self, proc, index):
        if proc == 'ファイル開く(Open File)':
            # self.param_list[index] = []
            # self.param = ['./0000_img/opencv_logo.jpg']
            self.dummy_frame.destroy()
            self.app_child = OpenFile(
                self.param_list, master=self.appwindow, gui=True)
            param, dst_img = self.app_child.get_data()
            self.dstimg_list[index] = dst_img
            self.param_list[index] = param

            pass
        elif proc == 'ファイル保存(Save File)':
            param, dst_img = self.app_child.get_data()
            self.dstimg_list[index-1] = dst_img
            self.param_list[index-1] = param

            img = self.dstimg_list[index-1]
            # img = cv2.imread('./0000_img/opencv_logo.jpg')
            # param = []
            # param = ['./save.jpg']
            self.app_child = SaveFile(img, self.param_list[index], gui=True)
            pass
        elif proc == 'ぼかし (Average)':
            img = self.dstimg_list[index-1]
            # param = []
            # param = [15, 15]
            # self.dummy_frame.destroy()
            self.app_child.image_edit_frame.destroy()
            self.app_child = Average(
                img, self.param_list, master=self.appwindow, gui=True)

            pass
        pass


if __name__ == "__main__":
    app = App()
    app.run()
