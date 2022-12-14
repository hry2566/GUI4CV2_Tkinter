"""GUIベース"""
import tkinter as tk


class GuiBase:
    """GUIベースクラス"""

    def __init__(self, master=None):
        self.master = master
        # build ui
        if master is None:
            toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
            toplevel1.configure(height=200, width=200)
            self.image_edit_frame = tk.Frame(toplevel1)
        else:
            self.image_edit_frame = tk.Frame(master)

        self.image_edit_frame.configure(height=200, padx=5, pady=5, width=200)
        self.settings_frame = tk.LabelFrame(self.image_edit_frame)
        self.settings_frame.configure(height=200, text="settings", width=200)
        self.none_label = tk.Label(self.settings_frame)
        self.none_label.configure(text="none label")
        self.none_label.pack(side="top")
        self.settings_frame.pack(fill="y", side="left")
        self.image_view_frame = tk.LabelFrame(self.image_edit_frame)
        self.image_view_frame.configure(
            height=200, text="image view", width=200)
        self.canvas1 = tk.Canvas(self.image_view_frame)
        self.canvas1.pack(expand="true", fill="both", side="top")
        frame5 = tk.Frame(self.image_view_frame)
        frame5.configure(height=200, width=200)
        self.image_switch_btn = tk.Button(frame5)
        self.image_switch_btn.configure(text="button1")
        self.image_switch_btn.pack(side="right")
        self.image_reset_btn = tk.Button(frame5)
        self.image_reset_btn.configure(text="button2")
        self.image_reset_btn.pack(side="right")
        frame5.pack(fill="x", side="top")
        self.image_view_frame.pack(expand="true", fill="both", side="left")
        self.image_edit_frame.pack(expand="true", fill="both", side="top")

        if master is None:
            # Main widget
            self.mainwindow = toplevel1

    def dummy(self):
        """パブリックダミー関数"""

    def run(self):
        """実行関数"""
        if self.master is None:
            self.mainwindow.mainloop()


# if __name__ == "__main__":
#     app = GuiBase()
#     app.run()
