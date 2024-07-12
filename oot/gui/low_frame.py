#from msilib.schema import Control
import tkinter as tk
from tkinter import ttk, IntVar
from tkinter import Tk, font
from tkinter import colorchooser
from enum import Enum, auto

import googletrans
from googletrans import Translator
from httpcore import SyncHTTPProxy

from PIL import ImageTk, Image
from tkinter import END, scrolledtext

from oot.gui.subframes.remove_frame import RemoveFrame
from oot.gui.subframes.write_frame import WriteFrame


def choose_color():
    # variable to store hexadecimal code of color
    color_code = colorchooser.askcolor(title ="Choose color") 
    LowFrame.reset_color_of_button_in_write_tab(color=color_code[1])
#------------------------------------------------------------------------------
# Low frame : low side tabbed pane (tools)
#------------------------------------------------------------------------------
class LowFrame:

    def __init__(self, root):
        # create a notebook
        low_frm = ttk.Notebook(root)
        LowFrame.notebook = low_frm
        low_frm.bind("<<NotebookTabChanged>>", self.__tab_changed)
        
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
        
        # init remove tab
        remove_tab_content = RemoveFrame(remove_tab)
        
        # init write tab
        #self.__init_write_tab(write_tab)
        WriteFrame(write_tab)

    @classmethod
    def get_status_of_check_list_in_remove_tab(cls, idx):
        pass

    @classmethod
    def reset_remove_tab_data(cls, texts=None):
        pass

    @classmethod
    def reset_write_tab_data(cls, texts=None):
        pass

    @classmethod
    def reset_translation_target_text_in_write_tab(cls, text=None):
        pass

    @classmethod
    def reset_color_of_button_in_write_tab(cls, color='#FFFF00'):
        pass
    
    def __tab_changed(self, event):
        tab_idx = LowFrame.notebook.index(LowFrame.notebook.select())
        print(f'tab_idx={tab_idx}')
        
        if tab_idx == 1:
            # write text to original text area of write tab in low frame
            radiobuttons = LowFrame.write_tab_text_list
            if radiobuttons is not None and radiobuttons.radio_value is not None:
                selected_idx = radiobuttons.radio_value.get()
                target_string = LowFrame.write_tab_text_org.get("1.0",'end-1c')
                if selected_idx == 0 and target_string is None or len(target_string) == 0:
                    # write text to original text area of write tab in low frame
                    LowFrame.reset_translation_target_text_in_write_tab(radiobuttons.text_list[selected_idx])

class ScrollableListType(Enum):
    CHECK_BUTTON = auto()
    RADIO_BUTTON = auto()

class ScrollableList(tk.Frame):
    # note : the following 2 variables should be reset when image changes
    #        - list_values
    #        - text
    def __init__(self, root, list_type, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.list_type = list_type
        self.vsb = ttk.Scrollbar(self, orient="vertical")
        self.text = tk.Text(self, width=40, height=20, 
                            yscrollcommand=self.vsb.set)
        self.vsb.config(command=self.text.yview)
        self.vsb.pack(side="right", fill="y")
        self.text.pack(side="left", fill="both", expand=True)
        self.list_values = []

    def __get_indexed_text(self, idx, text):
        return str(idx) + '|' + text
    
    def reset(self, text_list=None):
        self.text.delete('1.0', END)
        self.list_values = []
        self.text_list = text_list
        print ('[LowFrame.ScrollableList] reset() called!!...')
        print ('[LowFrame.ScrollableList] reset() : text_list=', text_list)
        
        self.radio_value = None
        if text_list is not None:
            idx = 0
            self.radio_value = IntVar()
            self.list_values = [None] * len(text_list)
            for i in range(len(text_list)):
                self.list_values[i] = tk.BooleanVar()
            
            for t in text_list:
                if self.list_type == ScrollableListType.CHECK_BUTTON:
                    # Reference : checkbutton example getting value in callback
                    # - https://arstechnica.com/civis/viewtopic.php?t=69728
                    from oot.control.low_write_control import selectedCheckListInRemoveTab
                    cb = tk.Checkbutton(self, text=t, command=lambda i=self.__get_indexed_text(idx,t): selectedCheckListInRemoveTab(i), var=self.list_values[idx])
                elif self.list_type == ScrollableListType.RADIO_BUTTON:
                    from oot.control.low_write_control import selectedRadioListInRemoveTab
                    cb = tk.Radiobutton(self, text=t, command=lambda i=self.__get_indexed_text(idx,t): selectedRadioListInRemoveTab(i), variable=self.radio_value, value=idx)
                else:
                    cb = tk.Checkbutton(self, text=t)
                self.text.window_create("end", window=cb)
                self.text.insert("end", "\n") # to force one checkbox per line
                idx = idx + 1