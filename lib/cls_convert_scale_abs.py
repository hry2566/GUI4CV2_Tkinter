"""明るさ／コントラスト"""
import cv2

from lib.gui.cls_edit_window import EditWindow
from lib.parts.parts_scale import Parts_Scale


class ConvertScaleAbs(EditWindow):
    """明るさ／コントラストクラス"""

    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__alpha = 1
        self.__beta = 0
        self.__proc_flag = False
        self.__gui = gui

        if len(param) == 2:
            self.__alpha = param[0]
            self.__beta = param[1]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__convert_scale_abs()

        if gui:
            self.draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = Parts_Scale(self.settings_frame)
        self.__scale1.configure(
            label='contrast', side='top', from_=1, to=3, resolution=0.01)

        self.__scale2 = Parts_Scale(self.settings_frame)
        self.__scale2.configure(
            label='brightness', side='top', from_=-128, to=128)

        self.__scale1.set(self.__alpha)
        self.__scale2.set(self.__beta)

    def __init_events(self):
        self.__scale1.bind(changed=self.__on_scale)
        self.__scale2.bind(changed=self.__on_scale)

    def __on_scale(self):
        if self.__proc_flag:
            return
        self.__proc_flag = True
        self.__alpha = self.__scale1.get()
        self.__beta = self.__scale2.get()
        self.dst_img = self.__convert_scale_abs()
        self.draw()
        self.__proc_flag = False

    def __convert_scale_abs(self):
        img = cv2.convertScaleAbs(
            self.origin_img, alpha=self.__alpha, beta=self.__beta)
        return img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.__alpha)
        param.append(self.__beta)
        if self.__gui:
            print('Proc : ConvertScaleAbs')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     img = cv2.imread('./0000_img/opencv_logo.jpg')
#     param = []
#     param = [3.0, 128]
#     app = ConvertScaleAbs(img, param, gui=True)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./ConvertScaleAbs.jpg', dst_img)
