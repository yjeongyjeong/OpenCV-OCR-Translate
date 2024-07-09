from tkinter import messagebox as mb

from oot.data.data_manager import DataManager
from oot.gui.low_frame import LowFrame
from oot.gui.middle_frame import MiddleFrame


def selectedRadioListInRemoveTab(text):
    print ('[LowFrameControl] selectedRadioListInRemoveTab() called!!...')
    text_info = text.split('|', 1)

    # get selected item's info (id, text, status)
    selected_item_id = int(text_info[0])
    selected_item_text = text_info[1]
    print ('[LowFrameControl] selectedRadioListInRemoveTab() : id = ', selected_item_id)
    print ('[LowFrameControl] selectedRadioListInRemoveTab() : text = ', selected_item_text)

    # write text to original text area of write tab in low frame
    LowFrame.resetTranslationTargetTextInWriteTab(selected_item_text)

    MiddleFrame.resetCanvasImages(DataManager.folder_data.get_work_file().name)

def selectedCheckListInRemoveTab(text):
    print ('[LowFrameControl] selectedCheckListInRemoveTab() called!!...')
    text_info = text.split('|', 1)

    # get selected item's info (id, text, status)
    selected_item_id = int(text_info[0])
    selected_item_text = text_info[1]
    selected_item_status = LowFrame.getStatusOfCheckListInRemoveTab(selected_item_id)
    print ('[LowFrameControl] selectedCheckListInRemoveTab() : id = ', selected_item_id)
    print ('[LowFrameControl] selectedCheckListInRemoveTab() : text = ', selected_item_text)
    print ('[LowFrameControl] selectedCheckListInRemoveTab() : status = ', selected_item_status.get())
    MiddleFrame.resetCanvasImages(DataManager.folder_data.get_work_file().name)
