import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
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
        brightness_label = ttk.Label(edit_tab, text='Brightness:')
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
        separator.grid(row=0, column=1, rowspan=5, sticky='ns', padx=10)

        # 현재 대비 값 저장할 변수 초기화
        self.current_contrast = tk.DoubleVar()
        self.current_contrast.set(0)

        # 대비 조절 레이블 설정
        contrast_label = ttk.Label(edit_tab, text='Contrast:')
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
    

    def brightness_changed(self, event):
    # 밝기 값이 슬라이더에 의해 변경될 때 호출
        self.update_value(self.current_brightness, self.brightness_value_label)


    def contrast_changed(self, event):
        # 대비 값이 슬라이더에 의해 변경될 때 호출
        self.update_value(self.current_contrast, self.contrast_value_label)


    def update_value(self, variable, label):
        # 주어진 변수의 값을 레이블에 표시하고, 변경 사항을 이미지에 반영하는 공통 함수
        label.config(text=self.get_current_value(variable))
        self.apply_changes()


    def apply_changes(self):
        from oot.gui.middle_frame import MiddleFrame
        from oot.data.data_manager import DataManager
        """
        brightness_changed: 밝기 슬라이더의 값이 변경될 때 호출. 변경된 값을 레이블에 표시하고, 이미지에 적용
        contrast_changed: 대비 슬라이더의 값이 변경될 때 호출. 변경된 값을 레이블에 표시하고, 이미지에 적용.
        apply_changes: 밝기와 대비의 변경 사항을 이미지에 적용하고, 이를 사용자 인터페이스에 반영.
        
        """
        # out_file 경로 가져오기
        out_file = DataManager.get_output_file()

        # image 생성
        img = cv2.imread(out_file)

        # 밝기 조정
        img_cv2 = self.__change_brightness(img, value=int(self.current_brightness.get()))

        # 대비 조정
        img_cv2 = self.__change_contrast(img_cv2, contrast=int(self.current_contrast.get()))

        # image 변환
        img_conv = Image.fromarray(img_cv2)

        # image 를 CanvasWorker 의 out 쪽 image로 세팅
        MiddleFrame.out_canvas_worker.set_image(img_conv)
        MiddleFrame.redraw_canvas_images()


    # 밝기 조절 함수
    def __change_brightness(self, input_image, value=0):
        hsv = cv2.cvtColor(input_image, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        v = cv2.add(v, value)
        v[v > 255] = 255
        v[v < 0] = 0
        final_hsv = cv2.merge((h, s, v))
        result_image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2RGB)
        return result_image
    

    # 대비 조절 함수
    def __change_contrast(self, input_image, contrast=0):
        """
        Args:
            input_image (numpy.ndarray): cv2.imread() 함수의 리턴 값으로 image data 의 numpy array 값과 같다.
            contrast (int): -50 ~ 50 범위의 슬라이더 값을 입력받아 대비를 조절
        Returns:
            numpy.ndarray: 대비 조절이 적용된 image data 의 numpy array 값.

            alpha: 대비 조정을 위해 사용되는 스케일링 인자
            alpha는 0부터 2 사이의 값으로 조절되며, 1보다 크면 대비가 증가하고, 1보다 작으면 대비가 감소
        """
        # contrast 값을 alpha로 변환 (대비 증가 시 1보다 크고, 감소 시 1보다 작게)
        alpha = (contrast + 50) / 50.0
        # 이미지의 평균 밝기를 계산
        avg_luminance = np.mean(cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY))
        # 대비 조정을 위해 이미지에 스케일링을 적용
        result_image = cv2.convertScaleAbs(input_image, alpha=alpha, beta=(1 - alpha) * avg_luminance)
        return result_image
