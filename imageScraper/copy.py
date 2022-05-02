import os
import shutil

directory = os.fsencode(os.getcwd())
n = 0
for dir in os.listdir(directory):
    dirName = os.fsdecode(dir)
    list = dirName.split(',')
    if len(list) > 1:
        same = True
        for i in range(1, len(list)):
            if not list[0][0:2] == list[i].replace(' ', '', 1)[0:2]:
                same = False
        if same:
            print(dirName)
            for file in os.listdir(dir):
                fileName = os.fsdecode(file)
                shutil.copyfile(dirName + '\\' + fileName, 'C:\\Users\\Eugen\\Desktop\\CloudClassification\\mergedDataset' + '\\' + list[0][0:2] + '\\' + fileName)
    else:
        if dirName != 'imageScraper.py' and dirName != 'copy.py':
            print(dirName)
            for file in os.listdir(dir):
                fileName = os.fsdecode(file)
                shutil.copyfile(dirName + '\\' + fileName, 'C:\\Users\\Eugen\\Desktop\\CloudClassification\\mergedDataset' + '\\' + list[0][0:2] + '\\' + fileName)

# 2543 11
