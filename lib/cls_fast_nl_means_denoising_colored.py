"""ぼかし(FastNlMeansDenoisingColored)"""
import cv2

from lib.gui.cls_edit_window import EditWindow
from lib.parts.parts_scale import Parts_Scale


class FastNlMeansDenoisingColored(EditWindow):
    """ぼかし(FastNlMeansDenoisingColored)クラス"""

    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__h = 3
        self.__hcolor = 20
        self.__template_window_size = 5
        self.__search_window_size = 20
        self.__proc_flag = True
        self.__gui = gui

        if len(param) == 4:
            self.__h = param[0]
            self.__hcolor = param[1]
            self.__template_window_size = param[2]
            self.__search_window_size = param[3]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__fast_nl_means_denoising_colored()

        if gui:
            self.draw()
            self.__proc_flag = False
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = Parts_Scale(self.settings_frame)
        self.__scale1.configure(label='h', side='top', from_=1, to=20)
        self.__scale2 = Parts_Scale(self.settings_frame)
        self.__scale2.configure(label='hColor', side='top', from_=1, to=20)
        self.__scale3 = Parts_Scale(self.settings_frame)
        self.__scale3.configure(
            label='templateWindowSize', side='top', from_=1, to=10)
        self.__scale4 = Parts_Scale(self.settings_frame)
        self.__scale4.configure(label='searchWindowSize',
                                side='top', from_=1, to=10)

        self.__scale1.set(self.__h)
        self.__scale2.set(self.__hcolor)
        self.__scale3.set(self.__template_window_size)
        self.__scale4.set(self.__search_window_size)

    def __init_events(self):
        self.__scale1.bind(changed=self.__on_scale)
        self.__scale2.bind(changed=self.__on_scale)
        self.__scale3.bind(changed=self.__on_scale)
        self.__scale4.bind(changed=self.__on_scale)

    def __on_scale(self):
        if self.__proc_flag:
            return
        self.__proc_flag = True
        self.__wait_msg()
        self.settings_frame.after(10, self.__on_scale_proc)

    def __on_scale_proc(self):
        self.__h = self.__scale1.get()
        self.__hcolor = self.__scale2.get()
        self.__template_window_size = self.__scale3.get()
        self.__search_window_size = self.__scale4.get()
        self.dst_img = self.__fast_nl_means_denoising_colored()
        self.draw()
        self.__proc_flag = False

    def __wait_msg(self):
        height, _, _ = self.dst_img.shape
        self.dst_img = cv2.putText(self.dst_img,
                                   'wait...',
                                   (0, int(height/2)),
                                   cv2.FONT_HERSHEY_PLAIN,
                                   height/73,
                                   (0, 0, 255),
                                   int(height/300),
                                   cv2.LINE_AA)
        self.draw()

    def __fast_nl_means_denoising_colored(self):
        img = cv2.fastNlMeansDenoisingColored(
            self.origin_img,
            None,
            self.__h,
            self.__hcolor,
            self.__template_window_size,
            self.__search_window_size)
        return img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.__h)
        param.append(self.__hcolor)
        param.append(self.__template_window_size)
        param.append(self.__search_window_size)
        if self.__gui:
            print('Proc : FastNlMeansDenoisingColored')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     # img = cv2.imread('./0000_img/I.jpg')
#     img = cv2.imread('./0000_img/opencv_logo.jpg')
#     # img = cv2.imread('./0000_img/ECU/ECUlow_1.jpg')
#     param = []
#     param = [10, 20, 5, 10]
#     app = FastNlMeansDenoisingColored(img, param, gui=True)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./FastNlMeansDenoisingColored.jpg', dst_img)
