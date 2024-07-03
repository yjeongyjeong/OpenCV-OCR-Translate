import tkinter as tk
from tkinter import ttk

# 메인 애플리케이션 클래스
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # 창 제목 설정
        self.title("OCR Translate")

        # Notebook 위젯 생성
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')
        self.geometry('1200x600+20+20')
        # 4개의 탭 추가
        self.create_tabs()

        
    def create_tabs(self):
        # 첫 번째 탭
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text='지우기') #이름변경하기gui_main, oot>gui>, 

        # 두 번째 탭
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text='쓰기')
        

        # 세 번째 탭
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text='이미지편집')


        # 네 번째 탭
        tab4 = ttk.Frame(self.notebook)
        self.notebook.add(tab4, text='저작권보호')



    #이브랜치에 다시 하나 커밋, 구조바꿔서 다시 커밋


