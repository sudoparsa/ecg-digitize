import os
import shutil

path = 'C:\\Users\\Parsa\\Desktop\\ECG\\final\\ECG_Record\\'
out_path = 'C:\\Users\\Parsa\\Desktop\\ECG\\final\\metadata\\'
metadata_path = 'C:\\Users\\Parsa\\Desktop\\ECG\\final\\.paperecg\\671-3           _200509291122.jpg.json'

files = os.listdir(path)
for file in files:
    name, extension = file.split('.')
    shutil.copy(metadata_path, out_path + name + '-' + extension + '.json')