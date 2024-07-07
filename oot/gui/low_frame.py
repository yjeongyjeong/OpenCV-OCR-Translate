#from msilib.schema import Control
import tkinter as tk
from tkinter import ttk, IntVar
from tkinter import Tk, font
from tkinter import colorchooser

import googletrans
from googletrans import Translator
from httpcore import SyncHTTPProxy

from PIL import ImageTk, Image
from tkinter import END, scrolledtext

#------------------------------------------------------------------------------
# Low frame : low side tabbed pane (tools)
#------------------------------------------------------------------------------
class LowFrame:

    def __init__(self, root):
        # create a notebook
        low_frm = ttk.Notebook(root)
        LowFrame.notebook = low_frm
        low_frm.bind("<<NotebookTabChanged>>", self.__tabChanged)
        
        low_frm.pack(pady=10, fill='both')
        low_frm.config(height=220)

        # create frames
        remove_tab = ttk.Frame(low_frm, height=50)
        write_tab = ttk.Frame(low_frm, height=50)
        edit_tab = ttk.Frame(low_frm, height=50)
        mosaic_tab = ttk.Frame(low_frm, height=50)

        remove_tab.pack(fill='both', expand=True)
        write_tab.pack(fill='both', expand=True)
        edit_tab.pack(fill='both', expand=True)
        mosaic_tab.pack(fill='both', expand=True)


        # add frames to notebook
        low_frm.add(remove_tab, text='지우기')
        low_frm.add(write_tab, text='쓰기')
        low_frm.add(edit_tab, text='이미지편집')
        low_frm.add(mosaic_tab, text='모자이크')

    @classmethod
    def getStatusOfCheckListInRemoveTab(cls, idx):
        pass

    @classmethod
    def resetRemoveTabData(cls, texts=None):
        pass

    @classmethod
    def resetWriteTabData(cls, texts=None):
        pass

    @classmethod
    def resetTranslationTargetTextInWriteTab(cls, text=None):
        pass

    @classmethod
    def resetColorOfButtonInWriteTab(cls, color='#FFFF00'):
        pass
    
    def __tabChanged(self, event):
        tab_idx = LowFrame.notebook.index(LowFrame.notebook.select())
        print(f'tab_idx={tab_idx}')
