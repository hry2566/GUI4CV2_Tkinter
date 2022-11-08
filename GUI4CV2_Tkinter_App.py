import tkinter as tk

from lib.cls_lib import *


class App(App_Base):
    def __init__(self, master=None):
        super().__init__(master)
        self.__app_child = None
        self.__menu_list = []
        self.__proc_list = []
        self.__param_list = []
        self.__dstimg_list = []
        self.__code_list = []
        self.__img_array = []
        self.__img_names = []
        self.__task_index = 0
        self.__proc_flag = False

        self.__init_gui()
        self.__init_events()

    def __init_gui(self):
        self.appwindow.title('GUI4CV2_Tkinter')

        # ファイル開く(Open File)をtask_list先頭に追加
        self.task_list.insert(tk.END, 'ファイル開く(Open File)')
        self.__proc_list.append('ファイル開く(Open File)')
        self.__param_list.append([])
        self.__dstimg_list.append([])

        self.__code_list.append(self.__create_code('ファイル開く(Open File)'))
        self.optionmenu1["menu"].delete(0, "last")

        self.__menu_list.append('ファイル開く(Open File)')
        self.__menu_list.append('ファイル保存(Save File)')
        self.__menu_list.append('画像メモリ作成(Create IMG Memory)')
        self.__menu_list.append('画像メモリI/O(MemoryIO)')
        self.__menu_list.append('画像結合(ImageCombine)')
        self.__menu_list.append('濃淡補正 (MovingAve)')
        self.__menu_list.append('濃淡補正 (MovingAveColor)')
        self.__menu_list.append('濃淡補正 (ShadingApproximate)')
        self.__menu_list.append('濃淡補正 (ShadingBlur)')
        self.__menu_list.append('濃淡補正 (ShadingMediaBlur)')
        self.__menu_list.append('濃淡補正 (ShadingMediaBlurColor)')
        self.__menu_list.append('濃淡補正 (ShadingCustomFillter)')
        self.__menu_list.append('明るさ／コントラスト (ConvertScaleAbs)')
        self.__menu_list.append('ガンマ補正 (Gamma)')
        self.__menu_list.append('ホワイトバランス (WhiteBalance)')
        self.__menu_list.append('平坦化 (EqualizeHist)')
        self.__menu_list.append('色反転 (Bitwise Not)')
        self.__menu_list.append('明度反転 (Reverse Brightness)')
        self.__menu_list.append('回転 (Rotate)')
        self.__menu_list.append('射影変換 (warpPerspective)')
        self.__menu_list.append('切り抜き (Trim)')
        self.__menu_list.append('ぼかし (Average)')
        self.__menu_list.append('ぼかし (Blur)')
        self.__menu_list.append('ぼかし (Median Blur)')
        self.__menu_list.append('ぼかし (Gaussian_Blur)')
        self.__menu_list.append('ぼかし (Bilateral_Filter)')
        self.__menu_list.append('ぼかし (FastNlMeansDenoisingColored)')
        self.__menu_list.append('シャープ (Filter2D)')
        self.__menu_list.append('シャープ (UnSharp)')
        self.__menu_list.append('膨張 (Dilate)')
        self.__menu_list.append('収縮 (Erode)')
        self.__menu_list.append('モルフォロジー (Morphology)')
        self.__menu_list.append('二値化 (Threshold)')
        self.__menu_list.append('二値化 (inRange)')
        self.__menu_list.append('二値化 (Adaptive_Thresholed)')
        self.__menu_list.append('輪郭抽出 (Canny)')
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
        param, dst_img = self.__app_child.get_data()
        index = self.__task_index
        self.__param_list[index] = param
        self.__dstimg_list[index] = dst_img

        if self.task_list.get(index) == '画像メモリ作成(Create IMG Memory)':
            self.__img_array = param[0]
            self.__img_names = param[1]

    def __onDelBtn_Events(self, event):
        if self.task_list.curselection() == () or self.task_list.curselection()[0] == 0:
            print('del_cancel')
            return

        index = self.__task_index

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
        if self.task_list.curselection() == ():
            return

        self.__task_index = self.task_list.curselection()[0]

        if self.__proc_flag:
            return

        self.__proc_flag = True
        index = event.widget.curselection()
        if index == ():
            return
        self.__run_proc(event.widget.get(index), index[0], True)
        self.__proc_flag = False

    def __run_proc(self, proc, index, gui_flag):
        if not index == 0:
            if self.__dstimg_list[index-1] == []:
                return
            img = self.__dstimg_list[index-1]
            if len(img) == []:
                return
        try:
            self.dummy_frame.destroy()
            self.__app_child.image_edit_frame.destroy()
        except:
            pass

        if proc == 'ファイル開く(Open File)':
            self.__app_child = OpenFile(
                self.__param_list, master=self.appwindow, gui=gui_flag)

        elif proc == 'ファイル保存(Save File)':
            self.__app_child = SaveFile(
                img, self.__param_list[index], gui=gui_flag)

        elif proc == 'ぼかし (Average)':
            self.__app_child = Average(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '二値化 (Adaptive_Thresholed)':
            self.__app_child = Adaptive_Thresholed(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'ぼかし (Bilateral_Filter)':
            self.__app_child = Bilateral_Filter(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'ぼかし (Blur)':
            self.__app_child = Blur(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '輪郭抽出 (Canny)':
            self.__app_child = Canny(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '膨張 (Dilate)':
            self.__app_child = Dilate(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '収縮 (Erode)':
            self.__app_child = Erode(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'シャープ (Filter2D)':
            self.__app_child = Fillter2D(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'ぼかし (Gaussian_Blur)':
            self.__app_child = Gaussian_Blur(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '二値化 (inRange)':
            self.__app_child = InRange(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '輪郭抽出 (Laplacian)':
            self.__app_child = Laplacian(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'ぼかし (Median Blur)':
            self.__app_child = Median_Blur(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'モルフォロジー (Morphology)':
            self.__app_child = Morphology(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '回転 (Rotate)':
            self.__app_child = Rotate(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '輪郭抽出 (Sobel)':
            self.__app_child = Sobel(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '二値化 (Threshold)':
            self.__app_child = Threshold(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '切り抜き (Trim)':
            self.__app_child = Trim(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'シャープ (UnSharp)':
            self.__app_child = UnSharp(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '明るさ／コントラスト (ConvertScaleAbs)':
            self.__app_child = ConvertScaleAbs(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'ぼかし (FastNlMeansDenoisingColored)':
            self.__app_child = FastNlMeansDenoisingColored(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'ガンマ補正 (Gamma)':
            self.__app_child = Gamma(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == 'ホワイトバランス (WhiteBalance)':
            self.__app_child = WhiteBalance(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '平坦化 (EqualizeHist)':
            self.__app_child = EqualizeHist(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '色反転 (Bitwise Not)':
            self.__app_child = Bitwise_Not(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '明度反転 (Reverse Brightness)':
            self.__app_child = ReverseBrightness(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '濃淡補正 (MovingAve)':
            self.__app_child = Shading_MovingAve(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '濃淡補正 (MovingAveColor)':
            self.__app_child = Shading_Color_MovingAve(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '濃淡補正 (ShadingApproximate)':
            self.__app_child = Shading_Approximate(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '濃淡補正 (ShadingBlur)':
            self.__app_child = Shading_Blur(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '濃淡補正 (ShadingMediaBlur)':
            self.__app_child = Shading_MedianBlur(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '濃淡補正 (ShadingCustomFillter)':
            self.__app_child = Shading_CustomFillter(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '画像メモリ作成(Create IMG Memory)':
            if len(self.__param_list[index]) == 0:
                self.__param_list[index].append(self.__img_array)
                self.__param_list[index].append(self.__img_names)

            self.__app_child = Create_Img_Memory(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '射影変換 (warpPerspective)':
            self.__app_child = Rotate3D(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '画像メモリI/O(MemoryIO)':
            if len(self.__param_list[index]) == 0:
                memIO = ['', []]
                self.__param_list[index].append(self.__img_array)
                self.__param_list[index].append(self.__img_names)
                self.__param_list[index].append(memIO)

            self.__app_child = MemoryIO(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '画像結合(ImageCombine)':
            self.__app_child = ImageCombine(
                img, self.__param_list[index], master=self.appwindow, gui=gui_flag)

        elif proc == '濃淡補正 (ShadingMediaBlurColor)':
            self.__app_child = Shading_Color_MedianBlur(
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

        elif proc == '輪郭抽出 (Canny)':
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

        elif proc == 'ぼかし (FastNlMeansDenoisingColored)':
            code = 'FastNlMeansDenoisingColored(img, param, gui=False)'

        elif proc == 'ガンマ補正 (Gamma)':
            code = 'Gamma(img, param, gui=False)'

        elif proc == 'ホワイトバランス (WhiteBalance)':
            code = 'WhiteBalance(img, param, gui=False)'

        elif proc == '平坦化 (EqualizeHist)':
            code = 'EqualizeHist(img, param, gui=False)'

        elif proc == '色反転 (Bitwise Not)':
            code = 'Bitwise_Not(img, param, gui=False)'

        elif proc == '明度反転 (Reverse Brightness)':
            code = 'ReverseBrightness(img, param, gui=False)'

        elif proc == '濃淡補正 (MovingAve)':
            code = 'Shading_MovingAve(img, param, gui=False)'

        elif proc == '濃淡補正 (MovingAveColor)':
            code = 'Shading_Color_MovingAve(img, param, gui=False)'

        elif proc == '濃淡補正 (ShadingApproximate)':
            code = 'Shading_Approximate(img, param, gui=False)'

        elif proc == '濃淡補正 (ShadingBlur)':
            code = 'Shading_Blur(img, param, gui=False)'

        elif proc == '濃淡補正 (ShadingMediaBlur)':
            code = 'Shading_MedianBlur(img, param, gui=False)'

        elif proc == '濃淡補正 (ShadingCustomFillter)':
            code = 'Shading_CustomFillter(img, param, gui=False)'

        elif proc == '画像メモリ作成(Create IMG Memory)':
            code += 'imgLib = Create_Img_Memory(img, [img_array, img_names], gui=False)'

        elif proc == '射影変換 (warpPerspective)':
            code = 'Rotate3D(img, param, gui=False)'

        elif proc == '画像メモリI/O(MemoryIO)':
            code = 'MemoryIO(img, param, gui=False)'

        elif proc == '画像結合(ImageCombine)':
            code = 'ImageCombine(img, param, gui=False)'

        elif proc == '濃淡補正 (ShadingMediaBlurColor)':
            code = 'Shading_Color_MedianBlur(img, param, gui=False)'

        return code

    def __onClick_create_code(self, event):
        memory_mode = 0

        pycode = ''
        for index, code in enumerate(self.__code_list):
            if code.endswith('imgLib = Create_Img_Memory(img, [img_array, img_names], gui=False)'):
                memory_mode = 1
            elif code == 'MemoryIO(img, param, gui=False)':
                memory_mode = 2
            else:
                memory_mode = 0

            if pycode == '':
                pycode = f'param = {str(self.__param_list[index])}\nimgLib = {code}'
            else:
                if memory_mode == 1:
                    pycode += '\n'
                    pycode += f'img_array = []\n'
                    pycode += f'img_names = {self.__img_names}\n'
                    pycode += 'param = [img_array, img_names]\n'
                    pycode += f'{code}'

                elif memory_mode == 2:
                    pycode += '\n' + \
                        f'memIO = {str(self.__param_list[index][2])}\n'
                    pycode += f'param = [img_array, img_names, memIO]\n'
                    pycode += f'imgLib = {code}'
                    pass
                else:
                    pycode += '\n' + \
                        f'param = {str(self.__param_list[index])}\nimgLib = {code}'

            pycode += '\nparam, img = imgLib.get_data()\n'
            if memory_mode == 1:
                pycode += 'img_array = param[0]\n'
                pycode += 'img_names = param[1]\n'
            elif memory_mode == 2:
                pycode += 'img_array = param[0]\n'

        str_import = 'from lib.cls_lib import * \n'

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
