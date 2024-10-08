"""編集画面"""
import platform

import cv2
import numpy as np
from PIL import Image, ImageOps, ImageTk

from lib.gui.cls_gui_base import GuiBase


class EditWindow(GuiBase):
    """編集画面クラス"""

    def __init__(self, img, master=None):
        super().__init__(master)
        self.origin_img = img
        self.dst_img = img
        self.__os_type = platform.system()
        self.__canvas_img = None
        self.__img_switch = True
        self.__draw_flag = False
        self.__view_scale = 1.0
        self.__start_x = 0
        self.__start_y = 0
        self.__imgpos_x = 0
        self.__imgpos_y = 0

        self.__init_gui()
        self.__init_events()
        self.draw()

    def __init_gui(self):
        self.none_label.configure(text='')
        self.image_switch_btn.configure(text='switch view\n(src)')
        self.image_reset_btn.configure(text='reset\n(scale&pos)')

    def __init_events(self):
        self.image_edit_frame.bind('<Configure>', self.__on_resize)
        self.image_switch_btn.bind('<1>', self.__on_switch_btn)
        self.image_reset_btn.bind('<1>', self.__on_reset_btn)
        if self.__os_type == 'Windows':
            self.canvas1.bind("<MouseWheel>", self.__mouse_wheel)
        elif self.__os_type == 'Linux':
            self.canvas1.bind("<ButtonPress-4>", self.__mouse_wheel)
            self.canvas1.bind("<ButtonPress-5>", self.__mouse_wheel)
        self.canvas1.bind('<2>', self.__mouse_wheel_down)
        self.canvas1.bind('<ButtonRelease-2>', self.__mouse_wheel_up)

    def __mouse_wheel_down(self, event):
        self.__start_x = event.x
        self.__start_y = event.y

    def __mouse_wheel_up(self, event):
        self.__imgpos_x -= self.__start_x - event.x
        self.__imgpos_y -= self.__start_y - event.y
        self.draw()

    def __mouse_wheel(self, event):
        wheel = True
        if self.__os_type == 'Windows':
            if event.delta > 0:
                wheel = True
            else:
                wheel = False
        elif self.__os_type == 'Linux':
            if event.num == 4:
                wheel = True
            elif event.num == 5:
                wheel = False

        if wheel:
            self.__view_scale += 0.05
        else:
            self.__view_scale -= 0.05
        self.draw()

    def __on_reset_btn(self, event):
        self.__view_scale = 1.0
        self.__imgpos_x = 0
        self.__imgpos_y = 0
        self.draw()

    def __on_switch_btn(self, event):
        if self.__img_switch:
            self.__img_switch = False
            self.image_switch_btn.configure(text='switch view\n(dst)')
        else:
            self.__img_switch = True
            self.image_switch_btn.configure(text='switch view\n(src)')
        self.draw()

    def __on_resize(self, event):
        self.draw()

    def get_view_scale(self):
        """画像表示倍率取得"""
        return self.__view_scale

    def get_img_pos(self):
        """画像表示位置取得"""
        return self.__imgpos_x, self.__imgpos_y

    def draw(self):
        """画像更新"""
        if self.__draw_flag:
            return
        self.__draw_flag = True

        if self.__img_switch:
            img = self.dst_img
        else:
            img = self.origin_img

        self.image_edit_frame.update()
        canvas_width = int(self.canvas1.winfo_width() * self.__view_scale)
        canvas_height = int(self.canvas1.winfo_height() * self.__view_scale)

        if 1 < canvas_width and 1 < canvas_height:
            # if img == []:
            #     img = np.zeros((1, 1, 3), np.uint8)
            cv_image = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(cv_image)
            try:
                pil_image = ImageOps.pad(
                    pil_image, (canvas_width, canvas_height))

                self.__canvas_img = ImageTk.PhotoImage(image=pil_image)

                self.canvas1.delete()
                self.canvas1.create_image(
                    canvas_width / 2 + self.__imgpos_x,
                    canvas_height / 2 + self.__imgpos_y,
                    image=self.__canvas_img)
            except:
                pass

        self.__draw_flag = False


def even2odd(number: int):
    """奇数化"""
    if number % 2 == 0:
        number += 1
    return number


# if __name__ == "__main__":
#     img = cv2.imread('./0000_img/opencv_logo.jpg')
#     app = EditWindow(img)
#     app.run()
