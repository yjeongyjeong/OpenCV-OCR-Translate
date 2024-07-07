import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

from oot.gui.top_frame import TopFrame
from oot.gui.middle_frame import MiddleFrame
from oot.gui.low_frame import LowFrame

# 메인 애플리케이션 클래스
class GuiManager:
    @staticmethod
    def init():
        # root window
        root = tk.Tk()
        root.geometry('1200x600+20+20')
        root.title('Image Text Master')

        # Top frame : top side buttons layout and command handlers
        GuiManager.top_frm = TopFrame(root)

        # Middle frame : middle side canvases
        GuiManager.mid_frm = MiddleFrame(root)

        # Low frame : low side tabbed pane (tools)
        GuiManager.low_frm = LowFrame(root)

        root.mainloop()