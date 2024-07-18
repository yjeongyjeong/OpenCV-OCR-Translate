from tkinter import ttk
from tkinter.scrolledtext import ScrolledText
from oot.gui.subframes.common import ScrollableList, ScrollableListType

class MosaicFrame:
    root = None
    def __init__(self, mosaic):
        # top button frame
        # mosaic_frm = ttk.Frame(mosaic)
        # mosaic_frm.pack(fill = 'both', side = 'left')
        # self.__init_mosaic_tab(mosaic)
        self.__init_mosaic_area_detection(mosaic)
        self.__init_mosaic_model_apply(mosaic)
        
    # ----------------------------------------------------------------
    # initial tab
    # ----------------------------------------------------------------     
    
    # def __init_mosaic_tab(self, mosaic):
    #     mosaic_tab_list = ScrollableList(mosaic, ScrollableListType.RADIO_BUTTON)
    #     mosaic_tab_list.text.config(width=80)
    #     mosaic_tab_list.pack(padx=2, pady=2, side="left", fill="y")
    #     mosaic_tab_list.reset()

    #     MosaicFrame.mosaic_tab_list = mosaic_tab_list
        
    # ----------------------------------------------------------------
    # mosaic area detection
    # ---------------------------------------------------------------- 
    
    def __init_mosaic_area_detection(self, mosaic_frm):
        a = ttk.LabelFrame(mosaic_frm, text='보호 영역 검출')
        a.pack(fill='both', side='left', expand=True)
        
        image_select = ttk.Button(a, text='보호 이미지 선택')
        image_select.grid(column=0, row=0, columnspan=1, sticky='W')
        
        mosaic_tab_list = ScrollableList(a, ScrollableListType.RADIO_BUTTON)
        mosaic_tab_list.text.config(width=100)
        # mosaic_tab_list.grid(column=0, row=1, columnspan=2, sticky='EW')
        mosaic_tab_list.reset()

        MosaicFrame.mosaic_tab_list = mosaic_tab_list
         
    # ----------------------------------------------------------------
    # mosaic model apply
    # ---------------------------------------------------------------- 
    def __init_mosaic_model_apply(self, mosaic_frm):
        b = ttk.LabelFrame(mosaic_frm, text='모자이크 적용')
        b.pack(fill='both', side='top')
        b.columnconfigure(0, weight=1)
        b.rowconfigure(0, weight=1)
        c = ttk.Frame(mosaic_frm)
        c.pack(side='bottom')
        
        mosaic_model = ttk.Label(b, text='모자이크 모델 선택')
        mosaic_model.grid(column=0, row=1, columnspan=2, sticky='W')

        combo_box = ttk.Combobox(b)
        combo_box.grid(column=0, row=1, columnspan=4, sticky='EW')
        
        # !콤보박스 예시 - 추후 수정
        font_size_list = tuple(range(5, 30))
        combo_box['values'] = font_size_list
        combo_box.current(5)
        # end!
        
        model_apply = ttk.Button(c, text='적용')
        model_apply.pack(side='left')
        model_cancel = ttk.Button(c, text='취소')
        model_cancel.pack(side='left')
            
            

        
    #     # mosaic area button
    #     mosaic_area = ttk.Button(self.mosaic_frm, text='모자이크 영역 검출')
    #     mosaic_area.pack(side='left')
    #     # mosaic model combobox
    #     mosaic_area = ttk.Button(self.mosaic_frm, text='모자이크 모델 선택')
    #     mosaic_area.pack(side='left')
        
    #     # a = ttk.Frame(low_frm_write_tab)
    #     # a.pack(side='right', fill='both')

    #     b = ttk.LabelFrame(a, text='스타일 도구')
    #     b.pack(fill='both', side='top')
    #     b.columnconfigure(0, weight=1)
    #     b.rowconfigure(0, weight=1)
    #     c = ttk.Frame(a)
    #     c.pack(side='bottom')

    #     write_tab_right_label_font_style = ttk.Label(b, text='폰트 스타일 :')
    #     write_tab_right_label_font_style.grid(column=0, row=0, columnspan=2, sticky=tk.W)
        
        
        
        
        
        
    #     label1 = tk.Label(master=root, text='Tkinter',bg='red',fg='white')
    #     label2 = tk.Label(master=root,text='Pack Layout',bg='green', fg='white')
    #     label3 = tk.Label(master=root, text='Demo',bg='blue', fg='white')

    #     label1.pack()
    #     label2.pack()
    #     label3.pack()

    #     btn_mosaic_area = ttk.Button(self.mosaic_frm, text = '모자이크 영역 검출', command = self.text_mosaic_area)
    #     btn_mosaic = ttk.Button(self.mosaic_frm, text = '모자이크 하기', command = self.text_mosaic)
    #     btn_mosaic_area.pack(side = 'left')
    #     btn_mosaic.pack(side = 'left')
        
    #     self.mosaic_tab_down_frm = ttk.Frame(mosaic)
    #     self.mosaic_tab_down_frm.pack(fill = 'both', expand = True)
        
    #     self.text = ScrolledText(self.mosaic_tab_down_frm)
    #     self.text.pack(fill = 'both', expand = True)

    #     MosaicFrame.root = self.mosaic_frm
    
    # def text_mosaic_area(self):
    #     self.text['state'] = 'normal'
    #     # ref: https://tkdocs.com/tutorial/text.html
    #     # 기존 글씨 삭제
    #     self.text.delete('1.0', 'end')
    #     self.text.insert('1.0', '모자이크 영역을 검출합니다.')
    #     # ref: https://www.pythontutorial.net/tkinter/tkinter-text/
    #     # 사용자가 위젯의 내용을 변경하지 못하도록 'disabled'
    #     self.text['state'] = 'disabled'
    
    # def text_mosaic(self):
    #     self.text['state'] = 'normal'
    #     self.text.delete('1.0', 'end')
    #     self.text.insert('1.0', '이미지 보호를 위해 모자이크를 진행합니다.')
    #     self.text['state'] = 'disabled'