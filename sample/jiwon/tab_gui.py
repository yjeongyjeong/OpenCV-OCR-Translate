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

        # 4개의 탭 추가
        self.create_tabs()

    def create_tabs(self):
        # 첫 번째 탭
        tab1 = ttk.Frame(self.notebook)
        self.notebook.add(tab1, text='지우기')
        label1 = tk.Label(tab1, text="지우기 탭입니다.")
        label1.pack(padx=10, pady=10)

        # 두 번째 탭
        tab2 = ttk.Frame(self.notebook)
        self.notebook.add(tab2, text='쓰기')
        label2 = tk.Label(tab2, text="쓰기 탭입니다.")
        label2.pack(padx=10, pady=10)

        # 세 번째 탭
        tab3 = ttk.Frame(self.notebook)
        self.notebook.add(tab3, text='이미지편집')
        label3 = tk.Label(tab3, text="이미지편집 탭입니다.")
        label3.pack(padx=10, pady=10)

        # 네 번째 탭
        tab4 = ttk.Frame(self.notebook)
        self.notebook.add(tab4, text='저작권보호')
        label4 = tk.Label(tab4, text="저작권 보호 탭입니다.")
        label4.pack(padx=10, pady=10)

# 애플리케이션 실행
if __name__ == "__main__":
    app = App()
    app.mainloop()


