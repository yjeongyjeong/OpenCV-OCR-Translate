import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

# 메인 애플리케이션 클래스
class App(tk.Tk):
    def __init__(self):
        super().__init__()

        # 창 제목 설정
        self.title("OCR Translate")
        self.geometry('1200x600+20+20')

        # Notebook 위젯 생성
        self.notebook = ttk.Notebook(self)
        self.notebook.pack(expand=True, fill='both')

        # 이미지 파일 리스트
        self.image_files = ['image/1.jpg', 'image/2.jpg', 'image/3.jpg', 'image/4.jpg']
        self.image_index = 0

        # 4개의 탭 추가
        self.create_tabs()

    def create_tabs(self):
        # 첫 번째 탭
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text='지우기')
        self.create_layout(tab1)
        
        # 두 번째 탭
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text='쓰기')
        self.create_image_tab(tab2)

        # 세 번째 탭
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text='이미지편집')
        self.create_layout(tab3)
        # 네 번째 탭
        tab4 = ttk.Frame(self.notebook)
        self.notebook.add(tab4, text='저작권보호')
        self.create_layout(tab4)
        

    def create_layout(self, parent):
        # 상단 프레임 (탑 버튼 부분)
        top_frame = tk.Frame(parent, height=50)
        top_frame.pack(side='top', fill='x')
        top_button = tk.Button(top_frame, text='Button 1')
        top_button.pack(side='left', anchor='nw')

        # 중간 프레임 (더미 레이블 추가)
        middle_frame = tk.Frame(parent)
        middle_frame.pack(side='top', expand=True, fill='both')
        dummy_label = tk.Label(middle_frame, text="여기에 내용이 들어갑니다.")
        dummy_label.pack(expand=True)

        # 하단 프레임 (버튼 부분)
        bottom_frame = tk.Frame(parent, height=50)
        bottom_frame.pack(side='top', fill='x')
        bottom_button = tk.Button(bottom_frame, text='Button 2')
        bottom_button.pack(side='left', anchor='sw')

    def create_image_tab(self, parent):
        # 상단 프레임 (탑 버튼 부분)
        top_frame = tk.Frame(parent, height=50)
        top_frame.pack(side='top', fill='x')
        top_button = tk.Button(top_frame, text='Next Image', command=self.next_image)
        top_button.pack(side='left', anchor='nw')

        # 중간 프레임 (이미지 부분)
        self.middle_frame = tk.Frame(parent)
        self.middle_frame.pack(side='top', expand=True, fill='both')

        # 첫 번째 이미지 로드 및 표시
        self.load_image()

        # 하단 프레임 (버튼 부분)
        bottom_frame = tk.Frame(parent, height=50)
        bottom_frame.pack(side='top', fill='x')
        bottom_button = tk.Button(bottom_frame, text='Button 2')
        bottom_button.pack(side='left', anchor='sw')

        # 중간 프레임의 크기 조절 이벤트 바인딩
        parent.bind('<Configure>', self.resize_image)

    def load_image(self):
        image_file = self.image_files[self.image_index]
        image = Image.open(image_file)
        self.image_tk = ImageTk.PhotoImage(image)
        if hasattr(self, 'image_label'):
            self.image_label.config(image=self.image_tk)
        else:
            self.image_label = tk.Label(self.middle_frame, image=self.image_tk)
            self.image_label.pack(expand=True)

    def next_image(self):
        self.image_index = (self.image_index + 1) % len(self.image_files)
        self.load_image()

    def resize_image(self, event):
        tab = event.widget
        if tab.winfo_children():
            middle_frame = tab.winfo_children()[1]
            if middle_frame.winfo_children():
                image_label = middle_frame.winfo_children()[0]
                new_width = middle_frame.winfo_width()
                new_height = middle_frame.winfo_height()
                image_file = self.image_files[self.image_index]
                image = Image.open(image_file)
                image = image.resize((new_width, new_height - 100), Image.Resampling.LANCZOS)
                resized_image = ImageTk.PhotoImage(image)
                image_label.config(image=resized_image)
                image_label.image = resized_image

