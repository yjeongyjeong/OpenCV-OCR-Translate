import cv2

from oot.data.data_manager import DataManager
from oot.gui.common import CanvasWorkerPostDrawListner, ScrollableListListener

class MosaicPostDrawHandler(CanvasWorkerPostDrawListner):
    def do_post_draw(self, canvas, scale_ratio, rectangle_ids):
        from oot.gui.subframes.mosaic_frame import MosaicFrame
        from oot.gui.low_frame import LowFrame
        # draw lines for selected text in check list of remove tab in LowFrame
        tab_idx = LowFrame.notebook.index(LowFrame.notebook.select())
        if tab_idx == 3:
            print('[MosaicPostDrawHandler] do_post_draw() called!!...')
            idx = 0
            list_values = MosaicFrame.mosaic_tab_face_list.list_values
            list_faces = DataManager.get_work_file().get_faces()
            if list_values == None or len(list_values) == 0 or list_faces == None or len(list_faces) == 0:
                return
            for index, item in enumerate(list_values):
                if item.get() == True:
                    # 새로운 사각형 그리기
                    pos_info = list_faces[index].get_position_info()
                    start_x = pos_info[0]
                    start_y = pos_info[1]
                    end_x = pos_info[2] + start_x
                    end_y = pos_info[3] + start_y

                    rectangle_id = canvas.create_rectangle(
                        int(scale_ratio*start_x),  # start x 
                        int(scale_ratio*start_y),  # start y
                        int(scale_ratio*end_x),    # end x
                        int(scale_ratio*end_y),    # end y
                        #outline='green'
                        outline='#00ff00'
                    )
                    # 사각형 ID를 CanvasWorker 인스턴스에 저장
                    rectangle_ids.append(rectangle_id)
                idx = idx + 1

class MosaicTextListHandler(ScrollableListListener):
    def selected_radio_list(self, text):
        pass

    def selected_check_list(self, text):
        print ('[MosaicTextListHandler] selected_check_list() called!!...')
        from oot.gui.middle_frame import MiddleFrame
        # 체크하는 경우(status =  True) 양쪽 이미지에 사각형 그리기
        MiddleFrame.redraw_canvas_images()

def search_faces():
    # 얼굴 검출 시작
    from oot.data.data_manager import DataManager
    image = cv2.imread(DataManager.get_output_file())
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    detected_faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))
    
    # 얼굴 검출 결과 DataManager에 저장
    DataManager.get_work_file().set_faces(detected_faces)

    # 저장된 face list 얻기
    faces_names = DataManager.get_work_file().get_faces_as_string()
    if faces_names == None or len(faces_names) == 0:
        return

    # face list 를 scrollable list 에 set
    from oot.gui.subframes.mosaic_frame import MosaicFrame
    scrollable_frame = MosaicFrame.get_face_list()
    scrollable_frame.reset(faces_names)