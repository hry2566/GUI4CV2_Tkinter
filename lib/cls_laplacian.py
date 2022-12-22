"""輪郭抽出（ラプラシアン）"""
import os

import cv2

from lib.gui.cls_edit_window import EditWindow, even2odd
from lib.parts.parts_scale import Parts_Scale


class Laplacian(EditWindow):
    """輪郭抽出（ラプラシアン）クラス"""

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

        self.dst_img = self.__laplacian()

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
        self.dst_img = self.__laplacian()
        self.draw()
        self.__proc_flag = False

    def __laplacian(self):
        img_copy = self.origin_img.copy()
        img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

        self.__kernel = even2odd(self.__kernel)
        img = cv2.Laplacian(img_copy, cv2.CV_64F, ksize=self.__kernel)
        cv2.imwrite('dummy.jpg', img)
        img = cv2.imread('dummy.jpg')
        os.remove('dummy.jpg')
        return img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.__kernel)
        if self.__gui:
            print('Proc : Laplacian')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     img = cv2.imread('./0000_img/opencv_logo.jpg')
#     param = []
#     param = [5]
#     app = Laplacian(img, param, gui=True)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./laplacian.jpg', dst_img)
