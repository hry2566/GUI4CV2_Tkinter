"""メディアンぼかし"""
import cv2

from lib.gui.cls_edit_window import EditWindow, even2odd
from lib.parts.parts_scale import Parts_Scale


class MedianBlur(EditWindow):
    """メディアンぼかしクラス"""

    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__kernel = 1
        self.__proc_flag = False
        self.__gui = gui

        if len(param) == 1:
            self.__kernel = param[0]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__median_blur()

        if gui:
            self.draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale = Parts_Scale(self.settings_frame)
        self.__scale.configure(label='kernel_x', side='top', from_=1, to=30)
        self.__scale.set(self.__kernel)

    def __init_events(self):
        self.__scale.bind(changed=self.__on_scale)

    def __on_scale(self):
        if self.__proc_flag:
            return
        self.__proc_flag = True
        self.__kernel = self.__scale.get()
        self.dst_img = self.__median_blur()
        self.draw()
        self.__proc_flag = False

    def __median_blur(self):
        img_copy = self.origin_img.copy()

        self.__kernel = even2odd(self.__kernel)
        img = cv2.medianBlur(img_copy, self.__kernel)
        return img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.__kernel)
        if self.__gui:
            print('Proc : Median Blur')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     img = cv2.imread('./0000_img/opencv_logo.jpg')
#     param = []
#     param = [8]
#     app = MedianBlur(img, param, gui=True)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./Median_Blur.jpg', dst_img)
