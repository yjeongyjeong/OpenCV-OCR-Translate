import glob
import os
import shutil
from PIL import ImageTk, Image
import sys
sys.path.append('.')
from oot.gui.middle_frame import MiddleFrame
from oot.gui.top_frame import TopFrame

# FolderData > FileData > TextData

class FolderData:
    
    def __init__(self, path):
        self.__folder = path
        self.__files = []
        self.__work_file = None
        self.__init_work_folder()

    def __init_work_folder(self):
        FILE_EXT = ['png', 'jpg', 'gif']
        target_files = []
        [target_files.extend(glob.glob(self.__folder + '/' + '*.' + e)) for e in FILE_EXT]

        for tf in target_files:
            self.__files.append(FileData(tf))

        if len(self.__files) == 0:
            return

        self.__work_file = self.__files[0]

    def get_work_file(self):
        return self.__work_file
    
    def set_work_file(self, target_file):
        self.__work_file = target_file
        
    def get_files(self):
        return self.__files
    
    def get_files_as_string(self):
        file_strings = []
        for f in self.__files:
            file_strings.append(f.get_file_name())
        return file_strings
    
    def get_folder_path(self):
        return self.__folder

class FileData:
    def __init__(self, file):
        self.__name = file
        self.__texts = []
        self.__is_ocr_executed = False

    def get_file_name(self):
        return self.__name

    def is_ocr_executed(self):
        return self.__is_ocr_executed        
        
    def set_ocr_texts(self, ocr_texts):
        """
        param ocr_texts: 
            ocr_texts 은 아래와 같은 형태의 data 구조로 들어온다.
            [
                ([[24, 48], [345, 48], [345, 109], [24, 109]], '下载手机天猫APP', 0.8471784057548907), 
                ([[24, 130], [368, 130], [368, 204], [24, 204]], '享388元礼包', 0.9837027854197318), 
                ([[190, 306], [290, 306], [290, 336], [190, 336]], '立即扫码', 0.9933473467826843), 
                ([[160, 348], [334, 348], [334, 372], [160, 372]], '下载手机天猫APP领福利', 0.858102917437849)
            ]
        """
        self.__texts = []
        for t in ocr_texts:
            self.__texts.append(TextData(t[0], t[1]))

    def get_ocr_texts(self):
        return self.__texts
    
    def get_ocr_text(self, index):
        return self.__texts[index]


class TextData:
    def __init__(self, text, position=None):
        self.__text = text
        self.__tr_text = None
        """
        OCR return example: 
            [
                ([[24, 48], [345, 48], [345, 109], [24, 109]], '下载手机天猫APP', 0.8471784057548907), 
                ([[24, 130], [368, 130], [368, 204], [24, 204]], '享388元礼包', 0.9837027854197318), 
                ([[190, 306], [290, 306], [290, 336], [190, 336]], '立即扫码', 0.9933473467826843), 
                ([[160, 348], [334, 348], [334, 372], [160, 372]], '下载手机天猫APP领福利', 0.858102917437849)
            ]
        position example: [[24, 48], [345, 48], [345, 109], [24, 109]]
        """
        self.__position_info = None  # Example: [[24, 48], [345, 48], [345, 109], [24, 109]]
        
    def set_tr_text_with_position(self, tr_text, position):
        self.__tr_text = tr_text
        self.__position_info = position
    
    def get_text(self):
        return self.__text

    def get_position_info(self):
        return self.__position_info

    def get_tr_text(self):
        return self.__tr_text
        
    
class DataManager:
    folder_data = None
    def init():
        curr_path = os.getcwd()
        default_image_path = curr_path + os.sep + "image"
        DataManager.reset_work_folder(target_folder=default_image_path)
        
    @classmethod
    def get_work_file(cls):
        return DataManager.folder_data.get_work_file() 
    
    @classmethod
    def set_work_file(cls, target_file):
        DataManager.folder_data.set_work_file(target_file)
        
    @classmethod
    def reset_work_folder(cls, target_folder='./image'):
        print ('[DataManager.reset] reset, target=', target_folder)
        target_path = os.path.abspath(target_folder)
        cls.folder_data = FolderData(target_path)
        cls.__init_output_folder(target_path)

    @classmethod
    def __init_output_folder(cls,target_folder):
        print ('[DataManager] initOutputFiles() called...')
        print ('[DataManager] initOutputFiles() : target_folder = ', target_folder)

        output_folder = os.path.join(target_folder + os.sep + '__OUTPUT_FILES__')
        print ('[DataManager] initOutputFiles() : output_folder = ', output_folder)

        # create output folder if not exist
        if os.path.isdir(output_folder) == False:
            os.makedirs(output_folder)
            print ('[DataManager] initOutputFiles() : output_folder newly created!')
        
        if target_folder == None or len(target_folder) == 0:
            print ('[DataManager] initOutputFiles() : no source files!')
            return
        
        # copy files to output folder if source image file doesn't exist in output folder
        target_images = [file_data.get_file_name() for file_data in cls.folder_data.get_files()]
        for src_file in target_images:
            src_file_name = os.path.basename(src_file)
            out_file = os.path.join(target_folder, '__OUTPUT_FILES__', src_file_name)
            if not os.path.isfile(out_file):
                shutil.copy(src_file, out_file)
                
    
    @classmethod
    def get_output_file(cls):
        print ('[DataManager] get_output_file() called...')

        out_file_dir = cls.folder_data.get_folder_path()
        out_file_name = os.path.basename(cls.folder_data.get_work_file().get_file_name())
        out_file = os.path.join(out_file_dir, '__OUTPUT_FILES__', out_file_name)
        
        return out_file
    
    @classmethod
    def save_output_file(cls, src_file, out_image):  #src_file 인자필요없음(로그확인용) - 추후에 삭제예정
        print ('[DataManager] save_output_file() called...')

        # out_image는 PIL의 Image 객체
        if out_image is None:
            print ('[DataManager] save_output_file() : image is None, it can not be saved!')

        # out_file은 path
        out_file = cls.get_output_file()
        print ('[DataManager] save_output_file() : src_file=', src_file)
        print ('[DataManager] save_output_file() : out_file=', out_file)

        if out_file is not None:
            if out_file.lower().endswith(("png")) == False:
                out_image.convert("RGB").save(out_file)
            else:
                out_image.save(out_file)
            print('[DataManager] save_output_file(): Image saved successfully!')
            return True
        return False

    @classmethod
    def get_prev_file(cls):
        img_file=DataManager.get_work_file()
        print('[DataManager] getPrevImageFile() called!!...')
        for i in range(len(cls.folder_data.get_files())):
            print('[DataManager] getPrevImageFile() i=', i, cls.folder_data.get_files()[i].get_file_name())
            if cls.folder_data.get_files()[i].get_file_name() == img_file.get_file_name():
                if i != 0:
                    print('[DataManager] getPrevImageFile() - image found : ', cls.folder_data.get_files()[i-1].get_file_name())
                    cls.set_work_file(cls.folder_data.get_files()[i-1])
                    return cls.folder_data.get_files()[i-1]
                else:
                    break
        print('[DataManager] getPrevImageFile() - image not found!!')
        return None

    @classmethod
    def get_next_file(cls):
        img_file=DataManager.get_work_file()
        print ('[DataManager] getNextImageFile() called!!...')
        for i in range(len(cls.folder_data.get_files())):
            print ('[DataManager] getNextImageFile() i=', i, ', curr_file=', img_file, ', compare=', cls.folder_data.get_files()[i].get_file_name())
            if cls.folder_data.get_files()[i].get_file_name() == img_file.get_file_name():
                if (i+1) < len(cls.folder_data.get_files()):
                    print ('[DataManager] getNextImageFile() - image found : ', cls.folder_data.get_files()[i+1].get_file_name())
                    return cls.folder_data.get_files()[i+1]
                else:
                    break
        print ('[DataManager] getNextImageFile() - image not found!!')
        return None


    @classmethod
    def changed_work_image(cls, work_file):
        
        print('[ControlManager.changedWorkImage] work_img=', work_file.get_file_name())
        DataManager.set_work_file(work_file) # 현재 작업 파일을 업데이트

        # Change images in canvases of 'MiddleFrame' with the 1st image of new dir
        MiddleFrame.reset_canvas_images(work_file)
        
        # Set new dir to 'TopFrame' at the label displaying work dir
        TopFrame.change_work_file(work_file)