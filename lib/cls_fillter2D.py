"""シャープ"""
import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow
from lib.parts.parts_scale import Parts_Scale


class Fillter2D(EditWindow):
    """シャープクラス"""

    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__kernel = 0
        self.__proc_flag = False
        self.__gui = gui

        if len(param) == 1:
            self.__kernel = param[0]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__fillter2d()

        if gui:
            self.draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = Parts_Scale(self.settings_frame)
        self.__scale1.configure(
            label='kernel', side='top', resolution=0.1, from_=1, to=10)
        self.__scale1.set(self.__kernel)

    def __init_events(self):
        self.__scale1.bind(changed=self.__on_scale)

    def __on_scale(self):
        if self.__proc_flag:
            return
        self.__proc_flag = True

        self.__kernel = self.__scale1.get()
        self.dst_img = self.__fillter2d()
        self.draw()
        self.__proc_flag = False

    def __fillter2d(self):
        img_copy = self.origin_img.copy()

        kernel = np.array([[-self.__kernel, -self.__kernel, -self.__kernel],
                           [-self.__kernel, 1+8*self.__kernel, -self.__kernel],
                           [-self.__kernel, -self.__kernel, -self.__kernel]])
        img = cv2.filter2D(img_copy, ddepth=-1, kernel=kernel)
        return img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.__kernel)
        if self.__gui:
            print('Proc : Fillter2D')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     img = cv2.imread('./0000_img/opencv_logo.jpg')
#     param = []
#     param = [3.2]
#     app = Fillter2D(img, param, gui=True)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./fillter2d.jpg', dst_img)
