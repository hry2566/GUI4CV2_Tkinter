"""App_Base"""
import pickle
import tkinter as tk
from functools import partial

from lib.cls_lib import *


class AppBase:
    """App_Baseクラス"""

    def __init__(self, master=None):
        self.__proc_list = []
        self.__param_list = []
        self.__dstimg_list = []
        self.__code_list = []
        self.proc_code_list = []
        self.fnc_list = []
        self.__task_index = 0
        self.__app_child = 0
        self.__img_array = []
        self.__img_names = []
        self.__proc_flag = False
        self.__run_flag = False

        # build ui
        self.toplevel2 = tk.Tk() if master is None else tk.Toplevel(master)
        self.toplevel2.configure(height=200, width=230)
        self.toplevel2.minsize(800, 400)
        self.menu3 = tk.Menu(self.toplevel2)
        self.menu_file = tk.Menu(self.menu3, tearoff="false")
        self.menu3.add(tk.CASCADE, menu=self.menu_file, label='File')
        self.menu_image = tk.Menu(self.menu3, tearoff="false")
        self.menu3.add(tk.CASCADE, menu=self.menu_image, label='Image')
        self.menu_color = tk.Menu(self.menu3, tearoff="false")
        self.menu3.add(tk.CASCADE, menu=self.menu_color, label='Color')
        self.menu_fillter = tk.Menu(self.menu3, tearoff="false")
        self.menu3.add(tk.CASCADE, menu=self.menu_fillter, label='Fillter')
        self.menu_memory = tk.Menu(self.menu3, tearoff="false")
        self.menu3.add(tk.CASCADE, menu=self.menu_memory, label='Memory')
        self.toplevel2.configure(menu=self.menu3)
        self.split_frame = tk.Frame(self.toplevel2)
        self.split_frame.configure(background="#d9d9d9", height=200, width=200)
        self.frame2 = tk.Frame(self.split_frame)
        self.frame2.configure(height=200, width=200)
        self.labelframe1 = tk.LabelFrame(self.frame2)
        self.labelframe1.configure(height=200, text='Task', width=200)
        self.frame3 = tk.Frame(self.labelframe1)
        self.frame3.configure(height=200, width=200)
        self.run_btn = tk.Button(self.frame3)
        self.run_btn.configure(compound="left", text=' Run Task_List')
        self.run_btn.pack(fill="x", padx=5, side="top")
        self.del_task_btn = tk.Button(self.frame3)
        self.del_task_btn.configure(text=' Delete Task')
        self.del_task_btn.pack(fill="x", padx=5, side="top")
        self.set_param_btn = tk.Button(self.frame3)
        self.set_param_btn.configure(text=' Set Param')
        self.set_param_btn.pack(fill="x", padx=5, side="top")
        self.frame3.pack(fill="both", pady=5, side="top")
        self.frame4 = tk.Frame(self.labelframe1)
        self.frame4.configure(height=200, width=200)
        self.frame1 = tk.Frame(self.frame4)
        self.frame1.configure(height=200, width=200)
        self.label2 = tk.Label(self.frame1)
        self.label2.configure(text='Task List')
        self.label2.pack(anchor="sw", side="left")
        self.list_clear_btn = tk.Button(self.frame1)
        self.list_clear_btn.configure(text='List All Clear')
        self.list_clear_btn.pack(anchor="e", side="top")
        self.frame1.pack(fill="x", padx=5, side="top")
        self.task_lst = tk.Listbox(self.frame4)
        self.task_lst.configure(activestyle="underline", width=35)
        self.task_lst.pack(expand="true", fill="both", padx=5, side="top")
        self.frame4.pack(expand="true", fill="both", side="top")
        self.labelframe1.pack(
            anchor="w",
            expand="true",
            fill="y",
            padx=5,
            side="top")
        self.labelframe2 = tk.LabelFrame(self.frame2)
        self.labelframe2.configure(height=200, text='Python Code', width=200)
        self.create_code_btn = tk.Button(self.labelframe2)
        self.create_code_btn.configure(text='Create Code')
        self.create_code_btn.pack(fill="x", padx=5, pady=5, side="top")
        self.labelframe2.pack(fill="x", padx=5, side="top")
        self.labelframe4 = tk.LabelFrame(self.frame2)
        self.labelframe4.configure(height=200, text='Settings File', width=200)
        self.load_settings_btn = tk.Button(self.labelframe4)
        self.load_settings_btn.configure(text='Load')
        self.load_settings_btn.pack(
            expand="true", fill="x", padx=5, pady=5, side="left")
        self.save_settings_btn = tk.Button(self.labelframe4)
        self.save_settings_btn.configure(text='Save')
        self.save_settings_btn.pack(
            expand="true", fill="x", padx=5, pady=5, side="left")
        self.labelframe4.pack(fill="x", padx=5, pady=5, side="top")
        self.frame2.pack(fill="y", side="left")
        self.dummy_frame = tk.LabelFrame(self.split_frame)
        self.dummy_frame.configure(height=200, text='settings', width=200)
        self.dummy_frame.pack(expand="true", fill="both", side="top")
        self.split_frame.pack(
            anchor="w",
            expand="true",
            fill="both",
            padx=5,
            pady=5,
            side="left")

        # Main widget
        self.appwindow = self.toplevel2

        # init
        self.appwindow.title('GUI4CV2_Tkinter')
        self.__init_events()

    def __init_gui(self):
        proc = 'ファイル開く(Open File)'
        self.task_lst.insert(tk.END, proc)
        self.task_lst.select_clear(first=0, last=self.task_lst.size()-1)

        self.__proc_list.append(proc)
        self.__param_list.append([])
        self.__dstimg_list.append([])
        self.__code_list.append(self.__create_code(proc))

    def __init_events(self):
        self.set_param_btn.bind('<1>', self.__on_set_param_events)
        self.del_task_btn.bind('<1>', self.__on_del_btn_events)
        self.create_code_btn.bind('<1>', self.__on_click_create_code)
        self.task_lst.bind("<<ListboxSelect>>",
                           self.__on_select_list_box_events)
        self.run_btn.bind("<1>", self.__on_click_run_task)
        self.load_settings_btn.bind("<1>", self.__on_click_load_settings)
        self.save_settings_btn.bind("<1>", self.__on_click_save_settings)
        self.list_clear_btn.bind("<1>", self.__on_click_list_clear)

    def set_menu(self, menu, items):
        """set_menu関数"""
        for item in items:
            menu.add_command(label=item, command=partial(
                self.__submenu_selected, item))

    def __submenu_selected(self, proc):
        if self.__dstimg_list[self.task_lst.size()-1] == []:
            return
        self.task_lst.insert(tk.END, proc)
        self.task_lst.select_clear(first=0, last=self.task_lst.size()-1)
        self.task_lst.select_set(self.task_lst.size()-1)
        self.__proc_list.append(proc)
        self.__param_list.append([])
        self.__dstimg_list.append([])
        self.__code_list.append(self.__create_code(proc))
        self.__on_select_list_box_events(None)

    def set_proc_code(self, proc_code_list, fnc_list):
        """set_proc_code関数"""
        self.proc_code_list = proc_code_list
        self.fnc_list = fnc_list
        self.__init_gui()

    def __create_code(self, proc):
        col1 = [col[0] for col in self.proc_code_list]
        col2 = [col[1] for col in self.proc_code_list]
        index = col1.index(proc)
        return col2[index]

    def __on_select_list_box_events(self, event):
        if self.task_lst.curselection() == ():
            return

        self.__task_index = self.task_lst.curselection()[0]

        if self.__proc_flag:
            return

        self.__proc_flag = True
        index = self.task_lst.curselection()
        if index == ():
            return
        self.__run_proc(self.task_lst.get(index), index[0], True)
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

        col1 = [col[0] for col in self.proc_code_list]
        fnc_index = col1.index(proc)

        if self.__run_flag:
            gui_flag = False

        if proc == '画像メモリ作成(Create IMG Memory)':
            if len(self.__param_list[index]) == 0:
                self.__param_list[index].append(self.__img_array)
                self.__param_list[index].append(self.__img_names)

            self.__app_child = self.fnc_list[fnc_index](
                img, self.__param_list[index], master=self.split_frame, gui=gui_flag)
        elif proc == '画像メモリI/O(MemoryIO)':
            if len(self.__param_list[index]) == 0:
                mem_io = ['', []]
                self.__param_list[index].append(self.__img_array)
                self.__param_list[index].append(self.__img_names)
                self.__param_list[index].append(mem_io)

            self.__app_child = self.fnc_list[fnc_index](
                img, self.__param_list[index], master=self.split_frame, gui=gui_flag)
        elif proc == 'ファイル開く(Open File)':
            self.__app_child = self.fnc_list[fnc_index](
                self.__param_list[index], master=self.split_frame, gui=gui_flag)
        else:
            self.__app_child = self.fnc_list[fnc_index](
                img, self.__param_list[index], master=self.split_frame, gui=gui_flag)

    def __on_set_param_events(self, event):
        if self.__app_child == 0:
            print('set_param_cancel')
            return

        param, dst_img = self.__app_child.get_data()
        index = self.__task_index
        self.__param_list[index] = param
        self.__dstimg_list[index] = dst_img

        if self.task_lst.get(index) == '画像メモリ作成(Create IMG Memory)':
            self.__img_array = param[0]
            self.__img_names = param[1]

    def __on_click_run_task(self, event):
        self.appwindow.after(1, self.__run_task)

    def __run_task(self):
        self.__run_flag = True
        rows = 0
        for index, _ in enumerate(self.__proc_list):
            self.task_lst.select_clear(first=0, last=self.task_lst.size()-1)
            self.task_lst.select_set(index)
            self.__on_select_list_box_events(None)
            self.__on_set_param_events(None)
            rows = index
        self.__run_flag = False

        if (self.__proc_list[-1] == 'ファイル開く(Open File)' or
            self.__proc_list[-1] == 'ファイル保存(Save File)' or
            self.__proc_list[-1] == '画像メモリ作成(Create IMG Memory)' or
                self.__proc_list[-1] == '画像メモリI/O(MemoryIO)'):
            rows -= 1
        self.task_lst.select_clear(first=0, last=self.task_lst.size()-1)
        self.task_lst.select_set(rows)
        self.__on_select_list_box_events(None)

    def __on_del_btn_events(self, event):
        if self.task_lst.curselection() == () or self.task_lst.curselection()[0] == 0:
            print('del_cancel')
            return

        index = self.__task_index
        self.task_lst.delete(index)
        del self.__proc_list[index]
        del self.__param_list[index]
        del self.__dstimg_list[index]
        del self.__code_list[index]

    def __on_click_create_code(self, event):
        self.appwindow.after(1, self.__create_sourcecode)

    def __create_sourcecode(self):
        memory_mode = 0

        pycode = ''
        for index, code in enumerate(self.__code_list):
            if code.endswith('imgLib = CreateImgMemory(img, [img_array, img_names], gui=False)'):
                memory_mode = 1
            elif code == 'MemoryIO(img, param, gui=False)':
                memory_mode = 2
            elif code == 'CircleDetection(img, param, gui=False)':
                memory_mode = 3
            elif code == 'EdgeMeasurement(img, param, gui=False)' or code == 'EdgeCustom(img, param, gui=False)':
                memory_mode = 4
            elif code == 'Edge_Arc(img, param, gui=False)':
                memory_mode = 5
            else:
                memory_mode = 0

            if pycode == '':
                pycode = f'param = {str(self.__param_list[index])}\nimgLib = {code}'
            else:
                if memory_mode == 1:
                    pycode += '\n'
                    pycode += 'img_array = []\n'
                    pycode += f'img_names = {self.__img_names}\n'
                    pycode += 'param = [img_array, img_names]\n'
                    pycode += f'{code}'

                elif memory_mode == 2:
                    pycode += '\n' + \
                        f'memIO = {str(self.__param_list[index][2])}\n'
                    pycode += 'param = [img_array, img_names, memIO]\n'
                    pycode += f'imgLib = {code}'
                else:
                    pycode += '\n' + \
                        f'param = {str(self.__param_list[index])}\nimgLib = {code}'

            pycode += '\nparam, img = imgLib.get_data()\n'
            if memory_mode == 1:
                pycode += 'img_array = param[0]\n'
                pycode += 'img_names = param[1]\n'
            elif memory_mode == 2:
                pycode += 'img_array = param[0]\n'
            elif memory_mode == 3:
                pycode += 'center = param[-1][0]\n'
                pycode += 'radius = param[-1][1]\n'
            elif memory_mode == 4:
                pycode += 'for line in param[5]:\n'
                pycode += '    print(f\'x1={line[0]}, y1={line[1]}, x2={line[2]}, y2={line[3]}, \')\n'
            elif memory_mode == 5:
                pycode += 'center = param[0][0]\n'
                pycode += 'ang = param[2]\n'

        str_import = 'from lib.cls_lib import * \n'

        pycode = f'{str_import}\n\n{pycode}'

        root = tk.Tk()
        root.withdraw()
        directory = './'
        typ = [("Python", ".py")]
        file = tk.filedialog.asksaveasfilename(
            initialdir=directory, filetypes=typ)
        root.destroy()
        if len(file) == 0:
            return
        if not '.py' in file:
            file += '.py'

        code_file = open(file, 'w', encoding='utf-8')
        code_file.write(pycode)
        code_file.close()

    def __on_click_save_settings(self, event):
        self.appwindow.after(1, self.__save_settings)

    def __save_settings(self):
        root = tk.Tk()
        root.withdraw()
        directory = './'
        typ = [("DATA", ".data")]
        file = tk.filedialog.asksaveasfilename(
            initialdir=directory, filetypes=typ)
        root.destroy()
        if len(file) == 0:
            return
        if not '.data' in file:
            file += '.data'

        data = []
        data.append(self.__proc_list)
        data.append(self.__param_list)
        data.append(self.__code_list)
        data.append(self.__dstimg_list)
        data.append(self.__img_names)
        data_file = open(file, 'wb')
        pickle.dump(data, data_file)
        data_file.close

    def __on_click_load_settings(self, event):
        self.appwindow.after(1, self.__load_settings)

    def __load_settings(self):
        root = tk.Tk()
        root.withdraw()
        typ = [("DATA", ".data")]
        directory = './'
        file = tk.filedialog.askopenfilenames(
            filetypes=typ, initialdir=directory)
        root.destroy()
        if len(file) == 0:
            return
        path = file[0]

        data = []
        data_file = open(path, 'rb')
        data = pickle.load(data_file)
        data_file.close()

        self.__proc_list = data[0]
        self.__param_list = data[1]
        self.__code_list = data[2]
        self.__dstimg_list = data[3]
        self.__img_names = data[4]

        self.task_lst.delete(0, tk.END)
        for proc in self.__proc_list:
            self.task_lst.insert(tk.END, proc)

    def __on_click_list_clear(self, event):
        self.task_lst.delete(0, tk.END)
        self.__proc_list = []
        self.__param_list = []
        self.__dstimg_list = []
        self.__code_list = []
        self.__img_array = []
        self.__img_names = []
        self.__init_gui()

    def run(self):
        """run関数"""
        self.appwindow.mainloop()


# if __name__ == "__main__":
#     app = AppBase()
#     app.run()
