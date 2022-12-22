"""明度反転"""
import cv2

from lib.gui.cls_edit_window import EditWindow


class ReverseBrightness(EditWindow):
    """明度反転クラス"""

    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__gui = gui

        if gui:
            super().__init__(img, master)

        if len(param) == 1:
            pass
        else:
            pass

        if gui:
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__reverse_brightness()

        if gui:
            self.draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

    def __init_events(self):
        pass

    # def __on_click(self, event):
    #     pass

    # def __on_scale(self, events):
    #     pass

    def __reverse_brightness(self):
        img_copy = self.origin_img.copy()
        hue, saturation, value = cv2.split(
            cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV))
        value = 255-value
        img = cv2.cvtColor(
            cv2.merge((hue, saturation, value)), cv2.COLOR_HSV2BGR)
        return img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        if self.__gui:
            print('Proc : ReverseBrightness')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     img = cv2.imread('./0000_img/test.jpg')
#     param = [False, False, True]
#     app = ReverseBrightness(img, param, gui=True)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./ReverseBrightness.jpg', dst_img)
