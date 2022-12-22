"""色反転"""
import cv2

from lib.gui.cls_edit_window import EditWindow


class BitwiseNot(EditWindow):
    """色反転クラス"""

    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__gui = gui

        if len(param) == 0:
            pass
        else:
            pass

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__bitwise_not()

        if gui:
            self.draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

    def __init_events(self):
        pass

    # def __onScale(self, events):
    #     pass

    def __bitwise_not(self):
        img_copy = self.origin_img.copy()
        img = cv2.bitwise_not(img_copy)
        return img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        if self.__gui:
            print('Proc : Bitwise_Not')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     img = cv2.imread('./0000_img/I.jpg')
#     param = []
#     app = BitwiseNot(img, param, gui=True)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./Bitwise_Not.jpg', dst_img)
