from enum import Enum, auto
import tkinter as tk
from tkinter import END, IntVar, ttk

from abc import *

class ScrollableListListener(metaclass=ABCMeta):
    """
    ScrollableList() 생성 시 listener의 값으로 사용되는 추상 클래스. 상속하여 사용.

    methods:
        selected_check_list : ScrollableListType이 CHECK_BUTTON인 경우 실행.
        selected_radio_list : ScrollableListType이 RADIO_BUTTON인 경우 실행.
    """
    @abstractmethod
    def selected_check_list(text):
        pass
    @abstractmethod
    def selected_radio_list(text):
        pass

class ScrollableListType(Enum):
    CHECK_BUTTON = auto()
    RADIO_BUTTON = auto()

class ScrollableList(tk.Frame):
    # note : the following 2 variables should be reset when image changes
    #        - list_values
    #        - text
    def __init__(self, root, list_type, listener: ScrollableListListener, *args, **kwargs):
        tk.Frame.__init__(self, root, *args, **kwargs)
        self.root = root
        self.list_type = list_type
        self.listener = listener
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
        print ('[ScrollableList] reset() called!!...')
        print ('[ScrollableList] reset() : text_list=', text_list)
        
        # Initialize radio_value if necessary
        if self.list_type == ScrollableListType.CHECK_BUTTON:
            self.radio_value = None
            if text_list is not None:
                self.list_values = [tk.BooleanVar() for _ in range(len(text_list))]
        elif self.list_type == ScrollableListType.RADIO_BUTTON:
            self.radio_value = IntVar()
            if text_list and len(text_list) > 0:
                self.radio_value.set(0)  # Select the first radio button by default
    
        # Proceed if text_list is not None
        if text_list:
            idx = 0    
            for t in text_list:
                if self.list_type == ScrollableListType.CHECK_BUTTON:
                    # Reference : checkbutton example getting value in callback
                    # - https://arstechnica.com/civis/viewtopic.php?t=69728
                    cb = tk.Checkbutton(self, text=t, command=lambda i=self.__get_indexed_text(idx,t): self.listener.selected_check_list(i), var=self.list_values[idx])
                elif self.list_type == ScrollableListType.RADIO_BUTTON:
                    cb = tk.Radiobutton(self, text=t, command=lambda i=self.__get_indexed_text(idx,t): self.listener.selected_radio_list(i), variable=self.radio_value, value=idx)
                else:
                    cb = tk.Checkbutton(self, text=t)
                self.text.window_create("end", window=cb)
                self.text.insert("end", "\n") # to force one checkbox per line
                idx = idx + 1