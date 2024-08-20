
from parts_switch_button_base import PartsSwitchButtonBaseApp
import tkinter as tk


class PartsSwitchButton(PartsSwitchButtonBaseApp):
    __mem_width = 0
    __btn_state = False

    def __init__(self, master=None, callback=None):
        super().__init__(master)
        self.__callback = callback

        self.__init_gui()
        self.__init_events()

    # **************************************
    # init function
    # **************************************
    def __init_gui(self):
        self.scale_button['state'] = tk.DISABLED

    def __init_events(self):
        self.scale_button.bind('<ButtonRelease-1>', self.__on_click_btn)
        self.scale_button.bind('<Configure>', self.__on_change_width)

    # **************************************
    # events function
    # **************************************
    def __on_click_btn(self, event):
        state = self.scale_button.get()
        if self.__callback is not None:
            self.__handler(self.__callback, state)

    def __on_change_width(self, event):
        if self.__mem_width != event.width:
            self.__mem_width = event.width
            self.scale_button.configure(sliderlength=int(event.width / 2))

    # **************************************
    # private function
    # **************************************
    def __set_state(self, state):
        self.scale_button['state'] = tk.NORMAL
        if state:
            self.lbl_state.configure(text='ON')
            self.__btn_state = True
            self.scale_button.set(1)
        else:
            self.lbl_state.configure(text='OFF')
            self.__btn_state = False
            self.scale_button.set(0)
        self.scale_button.update()
        self.scale_button['state'] = tk.DISABLED

    def __handler(self, func, *args):
        return func(*args)

    # **************************************
    # public function
    # **************************************
    def configure(self, label='', left=10, right=10):
        self.lbl.configure(text=label, width=left)
        self.lbl_state.configure(width=right)

    def get(self):
        return self.__btn_state

    def set(self, state):
        self.__set_state(state)


if __name__ == '__main__':
    # toplevel1 = tk.Tk() if master is None else master

    root = tk.Tk()
    slide_btn1 = PartsSwitchButton(root)
    slide_btn1.configure(label='Camera', left=8, right=8)
    slide_btn2 = PartsSwitchButton(root)
    slide_btn2.configure(label='Dobot', left=8, right=8)
    root.mainloop()
