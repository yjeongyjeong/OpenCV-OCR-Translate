
from oot.data.data_manager import *
import sys
sys.path.append('.')


dm = DataManager()

fd = FolderData("./image")
print(f'num files={len(fd.files)}')

for index, f in enumerate(fd.files):
    print(f'  > file={fd.files[index].name}')

texts = ["AAA", "BBB", "CCC"]
tr_texts = ["에이에이에이", "비비비", "씨씨씨"]

for f in fd.files:
    if f.is_ocr_detected:
        print(f'FILE={f.name}, texts={len(f.texts)}')
    else:
        print(f'FILE={f.name}, texts=None')

work_file = cast(FileData, fd.get_work_file())
print(f'work file==>{work_file.name}')
print(f'texts in work file : {len(work_file.texts)}')

work_file.set_texts(texts)
print(f'texts in work file : {len(work_file.texts)}')

work_file.texts[1].set_tr_text(tr_texts[1])
for index, t in enumerate(work_file.texts):
    print(f'  > text={t.text}, tr_text={t.tr_text}')