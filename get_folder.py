import pandas as pd
import os
from time import strftime

def get_folder(nclass):
    folderdf = pd.read_excel('classes.xlsx',sheet_name='Folders')
    folderdf.index = folderdf.iloc[:,0]
    return folderdf.loc[nclass]

def get_class(wkd,tm):
    classdf = pd.read_excel('classes.xlsx',sheet_name='Classes')
    if tm in list(classdf.Time):
        print('Found!')
        nclass = classdf[(classdf.Time == tm)].loc[:,wkd]
        return list(nclass)[0]
    else:
        return 0

def open_folder_scheduled():
    while True:
        tm = strftime('%H:%M')
        wkd = strftime('%a')
        nclass = get_class(wkd,tm)
        if nclass:
            folder = get_folder(nclass)
            os.system('explorer '+folder[1])
            print('folder opened')
            break
open_folder_scheduled()
    

