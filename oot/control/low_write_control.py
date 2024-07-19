from tkinter import messagebox as mb

from oot.data.data_manager import DataManager
from oot.gui.low_frame import LowFrame
from oot.gui.middle_frame import MiddleFrame


def selected_radio_list_in_remove_tab(text):
    print ('[LowFrameControl] selectedRadioListInRemoveTab() called!!...')
    text_info = text.split('|', 1)

    # get selected item's info (id, text, status)
    selected_item_id = int(text_info[0])
    selected_item_text = text_info[1]
    print ('[LowFrameControl] selectedRadioListInRemoveTab() : id = ', selected_item_id)
    print ('[LowFrameControl] selectedRadioListInRemoveTab() : text = ', selected_item_text)

    # write text to original text area of write tab in low frame
    LowFrame.reset_translation_target_text_in_write_tab(selected_item_text)

    MiddleFrame.reset_canvas_images(DataManager.get_work_file().get_file_name())

def selected_check_list_in_remove_tab(text):
    print ('[LowFrameControl] selectedCheckListInRemoveTab() called!!...')
    text_info = text.split('|', 1)

    # get selected item's info (id, text, status)
    selected_item_id = int(text_info[0])
    selected_item_text = text_info[1]
    selected_item_status = LowFrame.get_status_of_check_list_in_remove_tab(selected_item_id)
    print ('[LowFrameControl] selectedCheckListInRemoveTab() : id = ', selected_item_id)
    print ('[LowFrameControl] selectedCheckListInRemoveTab() : text = ', selected_item_text)
    print ('[LowFrameControl] selectedCheckListInRemoveTab() : status = ', selected_item_status.get())
    MiddleFrame.reset_canvas_images(DataManager.get_work_file().get_file_name())
