import tkinter as tk
from tkinter import ttk
from oot.data.data_manager import DataManager



#------------------------------------------------------------------------------
# Top frame : top side buttons layout and command handlers
#------------------------------------------------------------------------------
class TopFrame:
    root = None
    label_curr_file_name = None

    def __init__(self, root):
        top_frm = tk.Frame(root)
        top_frm.pack(padx=2, pady=2, fill='both', side='top')

        # top buttons : '이전 이미지', '다음 이미지', '폴더 변경'
        btn_change_folder = ttk.Button(top_frm, text='폴더 변경')
        

        label_curr_file_title = ttk.Label(top_frm, text='작업 파일:')
        label_curr_file_name = ttk.Label(top_frm, text=DataManager.folder_data.work_file.name)

        btn_change_folder.pack(side='left')
        label_curr_file_title.pack(side='left')
        label_curr_file_name.pack(side='left')
        
    @classmethod
    def changeWorkFile(cls, work_file):
        pass