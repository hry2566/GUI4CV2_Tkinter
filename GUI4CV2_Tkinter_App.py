import tkinter as tk

from lib.app.cls_app_base import App_Base
from lib.cls_adaptive_threshold import Adaptive_Thresholed
from lib.cls_average import Average
from lib.cls_bilateral_filter import Bilateral_Filter
from lib.cls_blur import Blur
from lib.cls_canny import Canny
from lib.cls_convert_scale_abs import ConvertScaleAbs
from lib.cls_dilate import Dilate
from lib.cls_erode import Erode
from lib.cls_fillter2D import Fillter2D
from lib.cls_gaussian_blur import Gaussian_Blur
from lib.cls_inrange import InRange
from lib.cls_laplacian import Laplacian
from lib.cls_median_blur import Median_Blur
from lib.cls_morphology import Morphology
from lib.cls_open_file import OpenFile
from lib.cls_rotate import Rotate
from lib.cls_save_file import SaveFile
from lib.cls_sobel import Sobel
from lib.cls_threshold import Threshold
from lib.cls_trim import Trim
from lib.cls_unsharp import UnSharp


class App(App_Base):
    def __init__(self, master=None):
        super().__init__(master)
        self.app_child = None
        self.__menu_list = []
        self.__proc_list = []
        self.__param_list = []
        self.__dstimg_list = []
        self.__code_list = []

        self.__init_gui()
        self.__init_events()

        # ファイル開く(Open File)をtask_list先頭に追加
        self.task_list.insert(tk.END, 'ファイル開く(Open File)')
        self.__proc_list.append('ファイル開く(Open File)')
        self.__param_list.append([])
        self.__dstimg_list.append([])
        self.__code_list.append(self.__create_code('ファイル開く(Open File)'))

    def __init_gui(self):
        self.appwindow.title('GUI4CV2_Tkinter')
        self.optionmenu1["menu"].delete(0, "last")
        self.__menu_list.append('ファイル開く(Open File)')
        self.__menu_list.append('ファイル保存(Save File)')
        self.__menu_list.append('明るさ／コントラスト (ConvertScaleAbs)')
        self.__menu_list.append('回転 (Rotate)')
        self.__menu_list.append('切り抜き (Trim)')
        self.__menu_list.append('ぼかし (Average)')
        self.__menu_list.append('ぼかし (Blur)')
        self.__menu_list.append('ぼかし (Median Blur)')
        self.__menu_list.append('ぼかし (Gaussian_Blur)')
        self.__menu_list.append('ぼかし (Bilateral_Filter)')
        self.__menu_list.append('シャープ (Filter2D)')
        self.__menu_list.append('シャープ (UnSharp)')
        self.__menu_list.append('膨張 (Dilate)')
        self.__menu_list.append('収縮 (Erode)')
        self.__menu_list.append('モルフォロジー (Morphology)')
        self.__menu_list.append('二値化 (Threshold)')
        self.__menu_list.append('二値化 (Canny)')
        self.__menu_list.append('二値化 (inRange)')
        self.__menu_list.append('二値化 (Adaptive_Thresholed)')
        self.__menu_list.append('輪郭抽出 (Laplacian)')
        self.__menu_list.append('輪郭抽出 (Sobel)')

    def __init_events(self):
        self.create_code_btn.bind('<1>', self.__onClick_create_code)

        for menu in self.__menu_list:
            self.optionmenu1["menu"].add_command(
                label=menu, command=tk._setit(self.tkvar, menu))

        self.add_btn.bind('<1>', self.__onAddBtn_Events)
        self.task_list.bind("<<ListboxSelect>>", self.__onSelectListBox_Events)
        self.set_param_btn.bind('<1>', self.__onSetParam_Events)
        self.del_btn.bind('<1>', self.__onDelBtn_Events)

    def __onSetParam_Events(self, event):
        param, dst_img = self.app_child.get_data()
        index = self.task_list.curselection()[0]
        self.__param_list[index] = param
        self.__dstimg_list[index] = dst_img

    def __onDelBtn_Events(self, event):
        if self.task_list.curselection() == () or self.task_list.curselection()[0] == 0:
            print('del_cancel')
            return
        index = self.task_list.curselection()[0]

        self.task_list.delete(index)
        del self.__proc_list[index]
        del self.__param_list[index]
        del self.__dstimg_list[index]
        del self.__code_list[index]
        pass

    def __onAddBtn_Events(self, event):
        task = self.tkvar.get()
        if task == '':
            print('add_cancel')
            return
        self.task_list.insert(tk.END, task)
        self.__proc_list.append(task)
        self.__param_list.append([])
        self.__dstimg_list.append([])
        self.__code_list.append(self.__create_code(task))

    def __onSelectListBox_Events(self, event):
        index = event.widget.curselection()
        self.__run_proc(event.widget.get(index), index[0], True)

    def __run_proc(self, proc, index, gui_flag):
        if not index == 0:
            if self.__dstimg_list[index-1] == []:
                return
            img = self.__dstimg_list[index-1]
            if img == []:
                return
        try:
            self.dummy_frame.destroy()
            self.app_child.image_edit_frame.destroy()
        except:
            pass

        if proc == 'ファイル開く(Open File)':
            self.app_child = OpenFile(
                self.__param_list, master=self.appwindow, gui=gui_flag)

        elif proc == 'ファイル保存(Save File)':
            self.app_child = SaveFile(
                img, self.__param_list[index], gui=gui_flag)

        elif proc == 'ぼかし (Average)':
            self.app_child = Average(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '二値化 (Adaptive_Thresholed)':
            self.app_child = Adaptive_Thresholed(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'ぼかし (Bilateral_Filter)':
            self.app_child = Bilateral_Filter(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'ぼかし (Blur)':
            self.app_child = Blur(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '二値化 (Canny)':
            self.app_child = Canny(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '膨張 (Dilate)':
            self.app_child = Dilate(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '収縮 (Erode)':
            self.app_child = Erode(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'シャープ (Filter2D)':
            self.app_child = Fillter2D(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'ぼかし (Gaussian_Blur)':
            self.app_child = Gaussian_Blur(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '二値化 (inRange)':
            self.app_child = InRange(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '輪郭抽出 (Laplacian)':
            self.app_child = Laplacian(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'ぼかし (Median Blur)':
            self.app_child = Median_Blur(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'モルフォロジー (Morphology)':
            self.app_child = Morphology(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '回転 (Rotate)':
            self.app_child = Rotate(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '輪郭抽出 (Sobel)':
            self.app_child = Sobel(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '二値化 (Threshold)':
            self.app_child = Threshold(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '切り抜き (Trim)':
            self.app_child = Trim(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'シャープ (UnSharp)':
            self.app_child = UnSharp(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '明るさ／コントラスト (ConvertScaleAbs)':
            self.app_child = ConvertScaleAbs(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

    def __create_code(self, proc):
        code = ''
        if proc == 'ファイル開く(Open File)':
            code = 'OpenFile(param, gui=False)'

        elif proc == 'ファイル保存(Save File)':
            code = 'SaveFile(img, param, gui=False)'

        elif proc == 'ぼかし (Average)':
            code = 'Average(img, param, gui=False)'

        elif proc == '二値化 (Adaptive_Thresholed)':
            code = 'Adaptive_Thresholed(img, param, gui=False)'

        elif proc == 'ぼかし (Bilateral_Filter)':
            code = 'Bilateral_Filter(img, param, gui=False)'

        elif proc == 'ぼかし (Blur)':
            code = 'Blur(img, param, gui=False)'

        elif proc == '二値化 (Canny)':
            code = 'Canny(img, param, gui=False)'

        elif proc == '膨張 (Dilate)':
            code = 'Dilate(img, param, gui=False)'

        elif proc == '収縮 (Erode)':
            code = 'Erode(img, param, gui=False)'

        elif proc == 'シャープ (Filter2D)':
            code = 'Fillter2D(img, param, gui=False)'

        elif proc == 'ぼかし (Gaussian_Blur)':
            code = 'Gaussian_Blur(img, param, gui=False)'

        elif proc == '二値化 (inRange)':
            code = 'InRange(img, param, gui=False)'

        elif proc == '輪郭抽出 (Laplacian)':
            code = 'Laplacian(img, param, gui=False)'

        elif proc == 'ぼかし (Median Blur)':
            code = 'Median_Blur(img, param, gui=False)'

        elif proc == 'モルフォロジー (Morphology)':
            code = 'Morphology(img, param, gui=False)'

        elif proc == '回転 (Rotate)':
            code = 'Rotate(img, param, gui=False)'

        elif proc == '輪郭抽出 (Sobel)':
            code = 'Sobel(img, param, gui=False)'

        elif proc == '二値化 (Threshold)':
            code = 'Threshold(img, param, gui=False)'

        elif proc == '切り抜き (Trim)':
            code = 'Trim(img, param, gui=False)'

        elif proc == 'シャープ (UnSharp)':
            code = 'UnSharp(img, param, gui=False)'

        elif proc == '明るさ／コントラスト (ConvertScaleAbs)':
            code = 'ConvertScaleAbs(img, param, gui=False)'

        return code

    def __onClick_create_code(self, event):
        pycode = ''
        for index, code in enumerate(self.__code_list):
            if pycode == '':
                pycode = f'param = {str(self.__param_list[index])}\nimgLib = {code}'
            else:
                print(index)
                pycode += '\n' + \
                    f'param = {str(self.__param_list[index])}\nimgLib = {code}'
            pycode += '\nparam, img = imgLib.get_data()\n'

        str_import = 'from lib.cls_adaptive_threshold import Adaptive_Thresholed \n'
        str_import += 'from lib.cls_average import Average \n'
        str_import += 'from lib.cls_bilateral_filter import Bilateral_Filter \n'
        str_import += 'from lib.cls_blur import Blur \n'
        str_import += 'from lib.cls_canny import Canny \n'
        str_import += 'from lib.cls_convert_scale_abs import ConvertScaleAbs \n'
        str_import += 'from lib.cls_dilate import Dilate \n'
        str_import += 'from lib.cls_erode import Erode \n'
        str_import += 'from lib.cls_fillter2D import Fillter2D \n'
        str_import += 'from lib.cls_gaussian_blur import Gaussian_Blur \n'
        str_import += 'from lib.cls_inrange import InRange \n'
        str_import += 'from lib.cls_laplacian import Laplacian \n'
        str_import += 'from lib.cls_median_blur import Median_Blur \n'
        str_import += 'from lib.cls_morphology import Morphology \n'
        str_import += 'from lib.cls_open_file import OpenFile \n'
        str_import += 'from lib.cls_rotate import Rotate \n'
        str_import += 'from lib.cls_save_file import SaveFile \n'
        str_import += 'from lib.cls_sobel import Sobel \n'
        str_import += 'from lib.cls_threshold import Threshold \n'
        str_import += 'from lib.cls_trim import Trim \n'
        str_import += 'from lib.cls_unsharp import UnSharp \n'

        pycode = f'{str_import}\n\n{pycode}'

        root = tk.Tk()
        root.withdraw()
        dir = './'
        file = tk.filedialog.asksaveasfilename(initialdir=dir)
        root.destroy()
        if len(file) == 0:
            path = ''
        else:
            path = file
            f = open(path, 'w', encoding='utf-8')
            f.write(pycode)
            f.close()
        pass


if __name__ == "__main__":
    app = App()
    app.run()
