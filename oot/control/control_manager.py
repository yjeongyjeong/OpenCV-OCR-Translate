import glob
import os

from oot.data.data_manager import DataManager
from oot.gui.low_frame import LowFrame
from oot.gui.middle_frame import MiddleFrame
from oot.gui.top_frame import TopFrame

class ControlManager:
    work_file = None

    def __init__(self):
        ControlManager.work_file = DataManager.folder_data.get_work_file()

    @classmethod
    def changed_work_image(cls, work_file):
        cls.work_file = work_file
        DataManager.folder_data.work_file = work_file  # 현재 작업 파일을 업데이트
        print('[ControlManager.changedWorkImage] work_img=', work_file)

        # Change images in canvases of 'MiddleFrame' with the 1st image of new dir
        MiddleFrame.reset_canvas_images(work_file)
        
        # Set new dir to 'TopFrame' at the label displaying work dir
        TopFrame.change_work_file(work_file)
