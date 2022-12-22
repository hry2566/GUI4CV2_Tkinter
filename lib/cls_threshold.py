"""二値化（Threshold）"""
import cv2

from lib.gui.cls_edit_window import EditWindow
from lib.parts.parts_scale import Parts_Scale


class Threshold(EditWindow):
    """二値化（Threshold）クラス"""

    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__thresh = 1
        self.__val = 255
        self.__proc_flag = False
        self.__gui = gui

        if len(param) == 2:
            self.__thresh = param[0]
            self.__val = param[1]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()
        self.dst_img = self.__threshold()

        if gui:
            self.draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = Parts_Scale(self.settings_frame)
        self.__scale1.configure(label='thresh', side='top', from_=1, to=255)
        self.__scale2 = Parts_Scale(self.settings_frame)
        self.__scale2.configure(label='val', side='top', from_=1, to=255)
        self.__scale1.set(self.__thresh)
        self.__scale2.set(self.__val)

    def __init_events(self):
        self.__scale1.bind(changed=self.__on_scale)
        self.__scale2.bind(changed=self.__on_scale)

    def __on_scale(self):
        if self.__proc_flag:
            return
        self.__proc_flag = True
        self.__thresh = self.__scale1.get()
        self.__val = self.__scale2.get()
        self.dst_img = self.__threshold()
        self.draw()
        self.__proc_flag = False

    def __threshold(self):
        img_copy = self.origin_img.copy()
        img_gray = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

        _, img = cv2.threshold(
            img_gray, self.__thresh, self.__val, cv2.THRESH_BINARY_INV)

        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.__thresh)
        param.append(self.__val)
        if self.__gui:
            print('Proc : Threshold')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     img = cv2.imread('./0000_img/opencv_logo.jpg')
#     param = []
#     param = [23, 255]
#     app = Threshold(img, param, gui=True)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./Threshold.jpg', dst_img)
