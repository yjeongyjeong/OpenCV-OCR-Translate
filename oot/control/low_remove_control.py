from oot.data.data_manager import DataManager


def clicked_search_text(): 
    print('[low_remove_control] clicked_search_text() called!!...')
    texts = DataManager.get_texts_from_image()
    print(f'[low_remove_control] clicked_search_text() result : {texts}')