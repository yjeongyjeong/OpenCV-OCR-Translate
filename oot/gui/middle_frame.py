import os
import tkinter as tk
from tkinter import ttk
from PIL import ImageTk, Image
import sys
sys.path.append('.')
from oot.gui.low_frame import LowFrame

#------------------------------------------------------------------------------
# Middle frame : middle side canvases
#------------------------------------------------------------------------------
class MiddleFrame:
    def __init__(self, root):
        # middle canvases frame
        mid_frm = tk.Frame(root)
        MiddleFrame.mid_frm = mid_frm
        mid_frm.pack(padx=2, pady=2, fill='both', expand=True)

        left_canvas = tk.Canvas(mid_frm, bg='lightgray')
        left_canvas.grid(row=0, column=0, sticky=tk.E+tk.W+tk.N+tk.S)
        right_canvas = tk.Canvas(mid_frm, bg='lightgray')
        right_canvas.grid(row=0, column=1, sticky=tk.E+tk.W+tk.N+tk.S)

        from oot.data.data_manager import DataManager
        src_file = DataManager.get_work_file().get_file_name()
        out_file = DataManager.get_output_file()

        # Reference :
        # - https://www.youtube.com/watch?v=xiGQD2J47nA
        # - https://github.com/flatplanet/Intro-To-TKinter-Youtube-Course/blob/master/image_bg_resize.py
        # - https://github.com/flatplanet/Intro-To-TKinter-Youtube-Course/
        def resizer(e):
            MiddleFrame.redraw_canvas_images()
 
        left_canvas.bind('<Configure>', resizer)
        # Added by Q&A from stackoverflow
        # https://stackoverflow.com/questions/72713209/how-to-keep-two-textboxes-the-same-size-when-resizing-window-with-python-tkinter
        mid_frm.columnconfigure((0,1), weight=1)
        mid_frm.rowconfigure(0, weight=1)

        from oot.gui.common import CanvasWorker
        MiddleFrame.src_canvas_worker = CanvasWorker(src_file, left_canvas)
        MiddleFrame.out_canvas_worker = CanvasWorker(out_file, right_canvas)

    @classmethod
    def temp_out_canvas_image(cls, temp_file):
        # temp_file을 임시적으로 out_file로 지정하여 출력하는 메소드(저장은 별개)
        print ('[MiddleFrame] temp_out_canvas_image() called...')
        cls.out_canvas_worker.change_image_file(temp_file)
        cls.redraw_canvas_images()

    @classmethod
    def redraw_canvas_images(cls):
        print ('[MiddleFrame.resizeCanvasImages] called...')
        cls.src_canvas_worker.draw_image()
        cls.out_canvas_worker.draw_image()

    @classmethod
    def get_adapted_image_size(cls, img_w, img_h, canvas_w, canvas_h):
        pass

    @classmethod
    def reset_canvas_images(cls, work_file):
        print ('[MiddleFrame] resetCanvasImages() called...')
        src_file = work_file.get_file_name()
        from oot.data.data_manager import DataManager
        out_file = DataManager.get_output_file()

        cls.src_canvas_worker.change_image_file(src_file)
        cls.out_canvas_worker.change_image_file(out_file)

        cls.src_canvas_worker.draw_image()
        cls.out_canvas_worker.draw_image()
    

    @classmethod
    def remove_selected_texts(cls):
        from oot.data.data_manager import DataManager
        print ('[MiddleFrame] remove_selected_texts() called...')
        image_index = DataManager.get_image_index()
        work_file = DataManager.folder_data.get_file_by_index(image_index) # FileData
        texts = work_file.get_texts_as_string()       # 해당 워크 파일에 해당하는 TextData의 text
        if texts == None:
            print ('[MiddleFrame] remove_selected_texts() : no texts were selected!')
            return None
        
        # Reference : Image conversion from cv2 to PhotoImage (PIL)
        # - https://m.blog.naver.com/heennavi1004/222028305376
        import cv2
        out_file = DataManager.get_output_file()
        positions = work_file.get_positions_as_string()
        img_cv2 = cls.__inpaint_for_selected_texts(out_file, positions)
        if img_cv2 is None:
            print ('[MiddleFrame] remove_selected_texts() : no need to redraw image!')
            return
        
        img_conv = Image.fromarray(img_cv2)

        # reset (redraw) output canvas with image which selected texts were removed in
        cls.out_canvas_worker.set_image(img_conv)
        cls.redraw_canvas_images()
    
    @classmethod
    def __inpaint_for_selected_texts(cls, img_path, texts_position):
        import numpy as np
        import cv2
        from oot.gui.subframes.remove_frame import RemoveFrame
        # texts # Example: [[24, 48], [345, 48], [345, 109], [24, 109]] => [y,x] 순서
        print ('[MiddleFrame] __inpaint_for_selected_texts() called...')

        # generate (word, box) tuples 
        img = cv2.cvtColor(cv2.imread(img_path), cv2.COLOR_BGR2RGB)
        mask = np.zeros(img.shape[:2], dtype="uint8")
        img_return = None
        idx = 0

        for t in texts_position:
            list_status = RemoveFrame.remove_tab_text_list.list_values
            if list_status[idx].get() == True:
                x0, y0 = t[0]
                x1, y1 = t[1]       # 왼쪽 상단 좌표 
                x2, y2 = t[2]
                x3, y3 = t[3]       # 오른쪽 하단 좌표 

                # 사각형 이미지 추출
                roi = img[y1:y3, x3:x1]

                # 그레이스케일 변환
                gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

                # 이진화 작업
                # Reference :
                # - https://gaussian37.github.io/vision-opencv-threshold/
                binary_roi = cv2.adaptiveThreshold(gray_roi, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 111, 2)

                # 모폴로지 적용
                kernel1 = cv2.getStructuringElement(cv2.MORPH_RECT, (9,9))
                img_morpho1 = cv2.morphologyEx(binary_roi, cv2.MORPH_CLOSE, kernel1)
                kernel2 = cv2.getStructuringElement(cv2.MORPH_RECT, (5,5))
                img_morpho2 = cv2.dilate(img_morpho1, kernel2, iterations=1)
                
                # mask에 이진화된 부분 삽입
                mask[y1:y3, x3:x1] = img_morpho2

                # inpaint 작업
                img_return = cv2.inpaint(img, mask, 7, cv2.INPAINT_NS)
            idx = idx+1
        return img_return
    
    @classmethod
    def apply_mosaic_to_selected_faces(cls):
        import cv2
        import numpy as np
        from oot.data.data_manager import DataManager
        from oot.gui.subframes.mosaic_frame import MosaicFrame
        from oot.control.low_mosaic_control import apply_mosaic
        print('[MiddleFrame] apply_mosaic_to_selected_faces() called...')
        
        # 데이터 관리자에서 작업 파일과 얼굴 데이터를 가져옴
        image_index = DataManager.get_image_index()
        work_file = DataManager.folder_data.get_file_by_index(image_index) # FileData
        faces = work_file.get_faces()  # 해당 워크 파일에 해당하는 FaceData의 좌표
        if faces is None:
            print('[MiddleFrame] apply_mosaic_to_selected_faces() : no faces were selected!')
            return None

        # 선택된 얼굴 영역 수집
        selected_faces = []
        list_values = MosaicFrame.mosaic_tab_face_list.list_values
        if list_values is None or len(list_values) == 0:
            print('[MiddleFrame] apply_mosaic_to_selected_faces() : no faces were selected in the list!')
            return

        for index, item in enumerate(list_values):
            if item.get() == True:
                pos_info = faces[index].get_position_info()
                selected_faces.append(pos_info)
        
        if not selected_faces:
            print('[MiddleFrame] apply_mosaic_to_selected_faces() : no faces selected for mosaic!')
            return

        # 현재 캔버스에 있는 이미지를 가져옴
        img_cv2 = cv2.cvtColor(np.array(cls.out_canvas_worker.get_image()), cv2.COLOR_RGB2BGR)

        # 모자이크 적용
        img_cv2 = apply_mosaic(img_cv2, selected_faces)

        # 업데이트된 이미지를 캔버스에 설정
        img_conv = Image.fromarray(cv2.cvtColor(img_cv2, cv2.COLOR_BGR2RGB))
        cls.out_canvas_worker.set_image(img_conv)
        cls.redraw_canvas_images()