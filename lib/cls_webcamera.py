"""WebCamera"""
import platform
import time
import tkinter as tk

import cv2
import numpy as np

from lib.app.cls_camera_base import CameraBase
from lib.gui.cls_edit_window import EditWindow


class WebCamera(EditWindow):
    """WebCameraクラス"""

    def __init__(self,  param, master=None, gui=False):
        self.origin_img = np.zeros((3, 3, 3)).astype('uint8') * 255
        self.dst_img = self.origin_img.copy()
        self.__gui = gui
        self.__camera = None
        self.__loop_flag = False
        self.__cap = None
        self.pf = platform.system()

        self.device_name = '/dev/video0'
        self.video_format = ''
        self.video_size = ''
        self.video_mode = 0

        if len(param) == 4:
            self.device_name = param[0]
            self.video_format = param[1]
            self.video_size = param[2]
            self.video_mode = param[3]

        if gui:
            super().__init__(self.origin_img, master)
            self.__init_gui()
            self.__init_events()
            self.draw()
            self.run()
        else:
            self.dst_img = self.__web_camera()

    def __init_gui(self):
        self.none_label.destroy()

        self.frame1 = tk.Frame(self.settings_frame)
        self.frame1.configure(height=200, width=200)
        self.device_frame = tk.LabelFrame(self.frame1)
        self.device_frame.configure(
            height=200, text='camera device', width=200)
        self.__camera_device = tk.StringVar()
        __values = [' ']
        self.device_opt_menu = tk.OptionMenu(
            self.device_frame, self.__camera_device, *__values, command=None)
        self.device_opt_menu.pack(fill="x", side="top")
        self.device_frame.pack(fill="x", padx=5, pady=5, side="top")
        self.formats_frame = tk.LabelFrame(self.frame1)
        self.formats_frame.configure(
            height=200, text='video formats', width=200)
        self.__camera_format = tk.StringVar()
        __values = [' ']
        self.format_opt_menu = tk.OptionMenu(
            self.formats_frame,
            self.__camera_format,
            *__values,
            command=None)
        self.format_opt_menu.pack(fill="x", side="top")
        self.formats_frame.pack(fill="x", padx=5, pady=5, side="top")
        self.image_size_frame = tk.LabelFrame(self.frame1)
        self.image_size_frame.configure(
            height=200, text='image size', width=200)
        self.__image_size = tk.StringVar()
        __values = [' ']
        self.image_size_opt_menu = tk.OptionMenu(
            self.image_size_frame, self.__image_size, *__values, command=None)
        self.image_size_opt_menu.pack(fill="x", side="top")
        self.image_size_frame.pack(fill="x", padx=5, pady=5, side="top")
        self.mode_frame = tk.LabelFrame(self.frame1)
        self.mode_frame.configure(height=200, text='mode', width=200)
        self.real_radio_btn = tk.Radiobutton(self.mode_frame)
        self.__radio_mode = tk.StringVar(value='1')
        self.real_radio_btn.configure(
            text='realtime', value=1, variable=self.__radio_mode, command=self.__on_selcect_radio)
        self.real_radio_btn.pack(expand="true", fill="x", side="left")
        self.shot_radio_btn = tk.Radiobutton(self.mode_frame)
        self.shot_radio_btn.configure(
            text='one shot', value=0, variable=self.__radio_mode, command=self.__on_selcect_radio)
        self.shot_radio_btn.pack(expand="true", fill="x", side="left")
        self.mode_frame.pack(fill="x", padx=5, pady=5, side="top")
        self.labelframe4 = tk.LabelFrame(self.frame1)
        self.labelframe4.configure(height=200, text='fps', width=200)
        self.entry_fps = tk.Entry(self.labelframe4)
        self.entry_fps.pack(fill="x", padx=5, pady=5, side="top")
        self.labelframe4.pack(fill="x", padx=5, pady=5, side="top")
        self.frame2 = tk.Frame(self.frame1)
        self.frame2.configure(height=200, width=200)
        self.start_btn = tk.Button(self.frame2)
        self.start_btn.configure(text='start')
        self.start_btn.pack(expand="true", fill="x", side="left")
        self.stop_btn = tk.Button(self.frame2)
        self.stop_btn.configure(text='stop')
        self.stop_btn.pack(expand="true", fill="x", side="left")
        self.frame2.pack(fill="x", padx=5, pady=5, side="top")
        self.frame1.pack(expand="true", fill="both", side="top")

        self.__init_camera()

    # init function ************************************************
    def __init_events(self):
        self.start_btn.bind('<1>', self.__on_click_start)
        self.stop_btn.bind('<1>', self.__on_click_stop)

    # def __onScale(self):
    #     pass

    # event function ***********************************************
    def __on_click_start(self, event):
        if self.__radio_mode.get() == '1':
            self.__loop_flag = True
            self.start_btn.configure(state="disable")
            self.real_radio_btn['state'] = 'disable'
            self.shot_radio_btn['state'] = 'disable'
            self.__cap.set(cv2.CAP_PROP_BUFFERSIZE, 4)
            self.frame1.after(1, self.__after_start)
        else:
            self.__cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            self.frame1.after(1, self.__after_shot)

    def __on_click_stop(self, event):
        self.__loop_flag = False
        self.start_btn.configure(state="normal")
        self.real_radio_btn['state'] = 'normal'
        self.shot_radio_btn['state'] = 'normal'

    def __on_select_device(self, event):
        self.device_name = self.__camera_device.get()
        device_num = int(self.__camera_device.get().replace('/dev/video', ''))

        if self.pf == 'Windows':
            self.__cap = None
            self.__cap = cv2.VideoCapture(device_num, cv2.CAP_DSHOW)
        elif self.pf == 'Linux':
            self.__cap = None
            self.__cap = cv2.VideoCapture(device_num)

        if self.__cap.isOpened():
            self.__set_format_list()
            self.__set_video_size_list()

    def __on_select_format(self, event):
        self.video_format = self.__camera_format.get()
        if self.__cap.isOpened():
            str_format = self.__camera_format.get()
            self.__cap.set(cv2.CAP_PROP_FOURCC,
                           cv2.VideoWriter_fourcc(*str_format))
            self.__set_video_size_list()

    def __on_select_image_size(self, event):
        self.video_size = self.__image_size.get()
        image_size = self.__image_size.get()
        height = int(image_size.split('x')[-1].split(' ')[0])
        width = int(image_size.split('x')[0].split(' ')[-1])
        fps = int(image_size.split(' ')[-1].replace('fps', ''))

        self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        self.__cap.set(cv2.CAP_PROP_FPS, fps)

    def __on_selcect_radio(self):
        self.video_mode = self.__radio_mode.get()

    # private function *********************************************
    def __after_shot(self):
        if self.__cap.isOpened():
            self.__cap.read()  # バッファー削除
            _, self.dst_img = self.__cap.read()
            self.draw()

    def __after_start(self):
        if self.__cap.isOpened():
            lap = 0
            start_time = time.time()
            while (self.__loop_flag):
                ret, self.dst_img = self.__cap.read()
                if not ret:
                    print('camera open error5')
                    self.__on_click_stop(None)
                else:
                    self.draw()
                    lap += 1
                    if (time.time()-start_time) > 1.0:
                        start_time = time.time()
                        self.entry_fps.delete(0, tk.END)
                        self.entry_fps.insert(0, lap)
                        lap = 0
        else:
            print('camera open error3')
            self.__on_click_stop(None)

    def __set_video_size_list(self):
        device_name = self.__camera_device.get()
        video_format = self.__camera_format.get()

        if self.pf == 'Windows':
            size_list = self.__camera.get_video_size_list_windows(
                self.__cap, device_name, video_format)
        elif self.pf == 'Linux':
            size_list = self.__camera.get_video_size_list(
                self.__cap, device_name, video_format)

        size_array = []
        for size in size_list:
            size_array.append(f'{size[0]}: {size[1]}x{size[2]} {size[3]}fps')

        if self.video_size == '':
            self.__image_size.set(size_array[0])
        else:
            self.__image_size.set(self.video_size)

        self.image_size_opt_menu.forget()
        self.image_size_opt_menu = tk.OptionMenu(self.image_size_frame,
                                                 self.__image_size,
                                                 *size_array,
                                                 command=self.__on_select_image_size)
        self.image_size_opt_menu.pack(fill="x", side="top")

    def __set_format_list(self):
        if self.__cap.isOpened():
            device_name = self.__camera_device.get()
            if self.pf == 'Windows':
                video_format = self.__camera.get_video_formats_list_windows(
                    self.__cap, device_name)
            elif self.pf == 'Linux':
                video_format = self.__camera.get_video_formats_list(
                    self.__cap, device_name)

            if len(video_format) != 0:
                self.format_opt_menu.forget()
                __values = video_format
                if self.video_format == '':
                    self.__camera_format.set(video_format[0])
                else:
                    self.__camera_format.set(self.video_format)

                self.format_opt_menu = tk.OptionMenu(
                    self.formats_frame,
                    self.__camera_format,
                    *__values,
                    command=self.__on_select_format)
                self.format_opt_menu.pack(fill="x", side="top")

    def __get_devices_list(self):
        self.__camera = CameraBase()

        if self.pf == 'Windows':
            devices = self.__camera.get_devices_list_windows()
        elif self.pf == 'Linux':
            devices = self.__camera.get_devices_list()

        if len(devices) != 0:
            self.device_opt_menu.forget()
            self.__values1 = devices
            self.__camera_device.set(self.device_name)

            self.device_opt_menu = tk.OptionMenu(self.device_frame,
                                                 self.__camera_device,
                                                 *self.__values1,
                                                 command=self.__on_select_device)
            self.device_opt_menu.pack(fill="x", side="top")
            return True
        return False

    def __init_camera(self):
        if self.__get_devices_list():
            device_num = int(
                self.device_name.replace('/dev/video', ''))

            if self.pf == 'Windows':
                self.__cap = cv2.VideoCapture(device_num, cv2.CAP_DSHOW)
            elif self.pf == 'Linux':
                self.__cap = cv2.VideoCapture(device_num)

            if self.__cap.isOpened():
                self.__set_format_list()
                self.__set_video_size_list()
                self.__on_select_format(None)
                self.__on_select_image_size(None)
                self.__radio_mode.set(self.video_mode)
                pass
            return True
        return False

    def __web_camera(self):
        img_copy = self.origin_img.copy()

        device_num = int(self.device_name.replace('/dev/video', ''))

        if self.pf == 'Windows':
            self.__cap = cv2.VideoCapture(device_num, cv2.CAP_DSHOW)
        elif self.pf == 'Linux':
            self.__cap = cv2.VideoCapture(device_num)

        if self.__cap.isOpened():
            self.__cap.set(cv2.CAP_PROP_FOURCC,
                           cv2.VideoWriter_fourcc(*self.video_format))

            height = int(self.video_size.split('x')[-1].split(' ')[0])
            width = int(self.video_size.split('x')[0].split(' ')[-1])
            fps = int(self.video_size.split(' ')[-1].replace('fps', ''))

            self.__cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
            self.__cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
            self.__cap.set(cv2.CAP_PROP_FPS, fps)

            if self.video_mode == 0:
                self.__cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
            else:
                self.__cap.set(cv2.CAP_PROP_BUFFERSIZE, 4)

            self.__cap.read()   # バッファ削除
            _, img_copy = self.__cap.read()
        return img_copy

    # public function **********************************************
    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        self.__loop_flag = False
        param = []
        param.append(self.device_name)
        param.append(self.video_format)
        param.append(self.video_size)
        param.append(self.video_mode)
        if self.__gui:
            print('Proc : WebCamera')
            print(f'param = {param}')
        return param, self.dst_img, self.__cap


if __name__ == "__main__":
    param = []
    param = ['/dev/video0', 'MJPG', 'MJPG: 640x480 30fps', '1']
    app = WebCamera(param, gui=False)
    param, dst_img, cap = app.get_data()

    _, img = cap.read()
    cv2.imwrite('./WebCamera.jpg', img)