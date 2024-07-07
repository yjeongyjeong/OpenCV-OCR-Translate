from msilib.schema import Control
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
        pass

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

from enum import Enum, auto
class ScrollableListType(Enum):
    CHECK_BUTTON = auto()
    RADIO_BUTTON = auto()

class ScrollableList(tk.Frame):
    def __init__(self, root, list_type, *args, **kwargs):
        pass

    def __getIndexedText(self, idx, text):
        pass
    
    def reset(self, text_list=None):
        pass