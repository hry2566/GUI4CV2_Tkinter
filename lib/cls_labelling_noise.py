"""ぼかし（移動平均）"""
import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow
from lib.parts.parts_labelling_noise import LabellingNoiseBaseApp


class LabellingNoise(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.min_width = 0
        self.max_width = 0
        self.min_height = 0
        self.max_height = 0
        self.min_area = 0
        self.max_area = 0

        self.__proc_flag = False
        self.__gui = gui

        if len(param) == 6:
            self.min_width = param[0]
            self.max_width = param[1]
            self.min_height = param[2]
            self.max_height = param[3]
            self.min_area = param[4]
            self.max_area = param[5]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.delete_nise()

        if gui:
            self.draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()
        self.ui_base = LabellingNoiseBaseApp(self.settings_frame)
        self.ui_base.width_min.set(self.min_width)
        self.ui_base.width_max.set(self.max_width)
        self.ui_base.height_min.set(self.min_height)
        self.ui_base.height_max.set(self.max_height)
        self.ui_base.area_min.set(self.min_area)
        self.ui_base.area_max.set(self.max_area)

    def __init_events(self):
        self.ui_base.spin_width_min.bind('<1>', self.__on_click_spin)
        self.ui_base.spin_width_min.bind('<Return>', self.__on_click_spin)
        self.ui_base.spin_width_max.bind('<1>', self.__on_click_spin)
        self.ui_base.spin_width_max.bind('<Return>', self.__on_click_spin)
        self.ui_base.spin_height_min.bind('<1>', self.__on_click_spin)
        self.ui_base.spin_height_min.bind('<Return>', self.__on_click_spin)
        self.ui_base.spin_height_max.bind('<1>', self.__on_click_spin)
        self.ui_base.spin_height_max.bind('<Return>', self.__on_click_spin)
        self.ui_base.spin_area_min.bind('<1>', self.__on_click_spin)
        self.ui_base.spin_area_min.bind('<Return>', self.__on_click_spin)
        self.ui_base.spin_area_max.bind('<1>', self.__on_click_spin)
        self.ui_base.spin_area_max.bind('<Return>', self.__on_click_spin)

    def __on_click_spin(self, event):
        # self.mainwindow.after(100, self.__click_spin)
        self.settings_frame.after(100, self.__click_spin)

    def __click_spin(self):
        self.min_width = self.ui_base.width_min.get()
        self.max_width = self.ui_base.width_max.get()
        self.min_height = self.ui_base.height_min.get()
        self.max_height = self.ui_base.height_max.get()
        self.min_area = self.ui_base.area_min.get()
        self.max_area = self.ui_base.area_max.get()

        self.dst_img = self.delete_nise()
        self.draw()

    def get_gray_image(self, img):
        if len(img.shape) == 3:
            img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        return img

    def get_bin_image(self, img):
        _, bin_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        return bin_img

    def delete_nise(self):
        src_img = self.origin_img.copy()
        gray_img = self.get_gray_image(src_img)
        bin_img = self.get_bin_image(gray_img)

        retval, labels, stats, _ = cv2.connectedComponentsWithStats(bin_img)
        h, w = src_img.shape[:2]
        mask = np.ones(retval, dtype=bool)
        for i in range(1, retval):
            if self.min_width < stats[i][2] < self.max_width or self.min_height < stats[i][3] < self.max_height or self.min_area < stats[i][4] < self.max_area:
                mask[i] = False
        filter_array = mask[labels.flatten()].reshape(h, w)
        src_img[~filter_array] = 0
        return src_img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.min_width)
        param.append(self.max_width)
        param.append(self.min_height)
        param.append(self.max_height)
        param.append(self.min_area)
        param.append(self.max_area)
        if self.__gui:
            print('Proc : LabellingNoise')
            print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./no1.png', 0)
    param = []
    param = [0, 0, 0, 0, 0, 0]
    app = LabellingNoise(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./labelling_Noise.jpg', dst_img)
