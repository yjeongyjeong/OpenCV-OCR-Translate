import glob
import os
from typing import cast

# FolderData > FileData > TextData

class FolderData:
    
    def __init__(self, path):
        self.folder = path
        self.files = []
        self.work_file = None
        self.__init_work_folder()

    def __init_work_folder(self):
        FILE_EXT = ['png', 'jpg', 'gif']
        target_files = []
        [target_files.extend(glob.glob(self.folder + '/' + '*.' + e)) for e in FILE_EXT]

        for tf in target_files:
            self.files.append(FileData(tf))

        if len(self.files) == 0:
            return

        self.work_file = self.files[0]

    def get_work_file(self):
        return self.work_file

class FileData:
    def __init__(self, file):
        self.name = file
        self.texts = []
        self.is_ocr_detected = False

    def set_texts(self, texts):
        self.texts = []
        for index, t in enumerate(texts):
            self.texts.append(TextData(t))

    def set_tr_text(self, index, tr_text):
        self.texts[index].text_ko = tr_text
    
    def get_text(self, index):
        return self.texts[index]

class TextData:
    def __init__(self, text):
        self.text = text
        self.tr_text = None

    def set_tr_text(self, tr_text):
        self.tr_text = tr_text

class DataManager:
    folder_data = None
    def __init__(self):
        curr_path = os.getcwd()
        default_image_path = curr_path + os.sep + "image"
        print(curr_path)
        print(default_image_path)
        DataManager.folder_data = FolderData(default_image_path)

