import tkinter as tk

from lib.cls_fillter2D import Fillter2D
from lib.app.cls_app_base import App_Base
from lib.cls_adaptive_threshold import Adaptive_Thresholed
from lib.cls_average import Average
from lib.cls_bilateral_filter import Bilateral_Filter
from lib.cls_blur import Blur
from lib.cls_canny import Canny
from lib.cls_dilate import Dilate
from lib.cls_erode import Erode
from lib.cls_open_file import OpenFile
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

        # ファイル開く(Open File)をtask_list先頭に追加
        self.task_list.insert(tk.END, 'ファイル開く(Open File)')
        self.proc_list.append('ファイル開く(Open File)')
        self.param_list.append([])
        self.dstimg_list.append([])

    def __init_gui(self):
        self.appwindow.title('GUI4CV2_Tkinter')
        self.optionmenu1["menu"].delete(0, "last")
        self.menu_list.append('ファイル開く(Open File)')
        self.menu_list.append('ファイル保存(Save File)')
        self.menu_list.append('ぼかし (Average)')
        self.menu_list.append('ぼかし (Blur)')
        self.menu_list.append('ぼかし (Bilateral_Filter)')
        self.menu_list.append('シャープ (Filter2D)')
        self.menu_list.append('膨張 (Dilate)')
        self.menu_list.append('収縮 (Erode)')
        self.menu_list.append('二値化 (Canny)')
        self.menu_list.append('二値化 (Adaptive_Thresholed)')

    def __init_events(self):
        for menu in self.menu_list:
            self.optionmenu1["menu"].add_command(
                label=menu, command=tk._setit(self.tkvar, menu))

        self.add_btn.bind('<1>', self.__onAddBtn_Events)
        self.task_list.bind("<<ListboxSelect>>", self.__onSelectListBox_Events)
        self.set_param_btn.bind('<1>', self.__onSetParam_Events)
        self.del_btn.bind('<1>', self.__onDelBtn_Events)

    def __onSetParam_Events(self, event):
        param, dst_img = self.app_child.get_data()
        index = self.task_list.curselection()[0]
        self.param_list[index] = param
        self.dstimg_list[index] = dst_img

    def __onDelBtn_Events(self, event):
        if self.task_list.curselection() == () or self.task_list.curselection()[0] == 0:
            print('del_cancel')
            return
        index = self.task_list.curselection()[0]

        self.task_list.delete(index)
        del self.proc_list[index]
        del self.param_list[index]
        del self.dstimg_list[index]
        pass

    def __onAddBtn_Events(self, event):
        task = self.tkvar.get()
        if task == '':
            print('add_cancel')
            return
        self.task_list.insert(tk.END, task)
        self.proc_list.append(task)
        self.param_list.append([])
        self.dstimg_list.append([])

    def __onSelectListBox_Events(self, event):
        index = event.widget.curselection()
        self.__run_proc(event.widget.get(index), index[0], True)

    def __run_proc(self, proc, index, gui_flag):
        if not index == 0:
            if self.dstimg_list[index-1] == []:
                return
            img = self.dstimg_list[index-1]
            if img == []:
                return
        try:
            self.dummy_frame.destroy()
            self.app_child.image_edit_frame.destroy()
        except:
            pass

        if proc == 'ファイル開く(Open File)':
            self.app_child = OpenFile(
                self.param_list, master=self.appwindow, gui=gui_flag)

        elif proc == 'ファイル保存(Save File)':
            self.app_child = SaveFile(
                img, self.param_list[index], gui=gui_flag)

        elif proc == 'ぼかし (Average)':
            self.app_child = Average(
                img, self.param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '二値化 (Adaptive_Thresholed)':
            self.app_child = Adaptive_Thresholed(
                img, self.param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'ぼかし (Bilateral_Filter)':
            self.app_child = Bilateral_Filter(
                img, self.param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'ぼかし (Blur)':
            self.app_child = Blur(
                img, self.param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '二値化 (Canny)':
            self.app_child = Canny(
                img, self.param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '膨張 (Dilate)':
            self.app_child = Dilate(
                img, self.param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '収縮 (Erode)':
            self.app_child = Erode(
                img, self.param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'シャープ (Filter2D)':
            self.app_child = Fillter2D(
                img, self.param_list[index], master=self.appwindow, gui=gui_flag)


if __name__ == "__main__":
    app = App()
    app.run()
