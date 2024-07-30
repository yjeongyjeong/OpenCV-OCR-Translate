import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk

#이미지 데이터를 배열로 처리하기 때문에 numpy 모듈필요
import numpy as np

class EditFrame:
    # EditFrame 클래스 초기화
    def __init__(self, edit_tab):

        # edit_tab 설정
        edit_tab.pack_propagate(False)
        edit_tab.columnconfigure(0, weight=1)
        edit_tab.columnconfigure(1, weight=0)
        edit_tab.columnconfigure(2, weight=1)
        edit_tab.rowconfigure(0, weight=1)
        edit_tab.rowconfigure(1, weight=0)

        # 현재 밝기 값 저장할 변수 초기화
        self.current_brightness = tk.DoubleVar()
        self.current_brightness.set(0)

        # 밝기 조절 레이블 설정
        brightness_label = ttk.Label(edit_tab, text='Contrast:')
        brightness_label.grid(row=0, column=0, padx=10, pady=(10, 5), sticky='ew')
        
        # 밝기 조절 슬라이더 설정
        brightness_slider = ttk.Scale(
            edit_tab,
            from_=-50,
            to=50,
            orient='horizontal',
            command=self.brightness_changed,
            variable=self.current_brightness,
            length=150
        )
        brightness_slider.grid(row=1, column=0, padx=10, pady=(5, 10), sticky='ew')

        # 현재 밝기 값 표시 레이블 설정
        brightness_value_label = ttk.Label(edit_tab, text='Current Value:')
        brightness_value_label.grid(row=2, column=0, padx=10, pady=(10, 5), sticky='s')
        self.brightness_value_label = ttk.Label(edit_tab, text=self.get_current_value(self.current_brightness))
        self.brightness_value_label.grid(row=3, column=0, padx=10, pady=(5, 10), sticky='s')

        # 구분선 설정
        separator = ttk.Separator(edit_tab, orient='vertical')
        separator.grid(row=0, column=1, rowspan=4, sticky='ns', padx=10)

        # 현재 대비 값 저장할 변수 초기화
        self.current_contrast = tk.DoubleVar()
        self.current_contrast.set(0)

        # 대비 조절 레이블 설정
        contrast_label = ttk.Label(edit_tab, text='Brightness:')
        contrast_label.grid(row=0, column=2, padx=10, pady=(10, 5), sticky='ew')
        
        # 대비 조절 슬라이더 설정
        contrast_slider = ttk.Scale(
            edit_tab,
            from_=-50,
            to=50,
            orient='horizontal',
            command=self.contrast_changed,
            variable=self.current_contrast,
            length=150
        )
        contrast_slider.grid(row=1, column=2, padx=10, pady=(5, 10), sticky='ew')

        # 현재 대비 값 표시 레이블 설정
        contrast_value_label = ttk.Label(edit_tab, text='Current Value:')
        contrast_value_label.grid(row=2, column=2, padx=10, pady=(10, 5), sticky='s')
        self.contrast_value_label = ttk.Label(edit_tab, text=self.get_current_value(self.current_contrast))
        self.contrast_value_label.grid(row=3, column=2, padx=10, pady=(5, 10), sticky='s')

    # 현재 변수 값 반환
    def get_current_value(self, variable):
        return f"{variable.get():.2f}"

    # 밝기 변경 시 호출되는 함수
    def brightness_changed(self, event):
        self.brightness_value_label.config(text=self.get_current_value(self.current_brightness))

    # 대비 변경 시 호출되는 함수
    def contrast_changed(self, event):
        self.contrast_value_label.config(text=self.get_current_value(self.current_contrast))

        from oot.gui.middle_frame import MiddleFrame
        from oot.data.data_manager import DataManager

        # out_file 경로 가져오기
        out_file = DataManager.get_output_file()

        # image 생성
        img = cv2.imread(out_file)

        # slider 의 값에 따른 brightness 조정
        img_cv2 = self.__change_brightness(img, value=int(float(event)))

        # image 변환
        img_conv = Image.fromarray(img_cv2)

        # image 를 CanvasWorker 의 out 쪽 image로 세팅
        from oot.gui.middle_frame import MiddleFrame
        
        # 이미지를 CanvasWorker 의 출력 쪽 이미지로 설정
        MiddleFrame.out_canvas_worker.set_image(img_conv)
        MiddleFrame.redraw_canvas_images()

    # 밝기 조절 함수
    def __change_brightness(self, input_image, value=0):
        """
        Reference: https://stackoverflow.com/questions/32609098/how-to-fast-change-image-brightness-with-python-opencv
        Args:
            input_image (numpy.ndarray): cv2.imread() 함수의 리턴 값으로 image data 의 numpy array 값과 같다.
            value (int, optional): -50 ~ 50
        Returns:
            numpy.ndarray: cv2.cvtColor() 함수의 리턴 값으로 image data 의 numpy array 값과 같다.

        """
        hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.add(v,value)
        v[v > 255] = 255
        v[v < 0] = 0
        final_hsv = cv2.merge((h, s, v))
        result_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)
        return result_image