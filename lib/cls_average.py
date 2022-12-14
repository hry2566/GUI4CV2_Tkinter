"""ぼかし（移動平均）"""
import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow
from lib.parts.parts_scale import Parts_Scale


class Average(EditWindow):
    """ぼかし（移動平均）クラス"""

    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__kernel_x = 1
        self.__kernel_y = 1
        self.__proc_flag = False
        self.__gui = gui

        if len(param) == 2:
            self.__kernel_x = param[0]
            self.__kernel_y = param[1]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__average()

        if gui:
            self.draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = Parts_Scale(self.settings_frame)
        self.__scale1.configure(label='kernel_x', side='top', from_=1, to=50)
        self.__scale2 = Parts_Scale(self.settings_frame)
        self.__scale2.configure(label='kernel_y', side='top', from_=1, to=50)

        self.__scale1.set(self.__kernel_x)
        self.__scale2.set(self.__kernel_y)

    def __init_events(self):
        self.__scale1.bind(changed=self.__onScale)
        self.__scale2.bind(changed=self.__onScale)

    def __onScale(self):
        if self.__proc_flag:
            return
        self.__proc_flag = True
        self.__kernel_x = self.__scale1.get()
        self.__kernel_y = self.__scale2.get()
        self.dst_img = self.__average()
        self.draw()
        self.__proc_flag = False

    def __average(self):
        kernel_x = self.__kernel_x
        kernel_y = self.__kernel_y
        kernel = np.ones((kernel_y, kernel_x), np.float32)/(kernel_x*kernel_y)
        img = cv2.filter2D(self.origin_img, -1, kernel)
        return img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.__kernel_x)
        param.append(self.__kernel_y)
        if self.__gui:
            print('Proc : Average')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     img = cv2.imread('./0000_img/opencv_logo.jpg')
#     param = []
#     param = [15, 15]
#     app = Average(img, param, gui=True)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./average.jpg', dst_img)
