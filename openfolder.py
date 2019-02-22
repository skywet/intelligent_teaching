import pandas as pd
import os
from time import strftime

def get_folder(nclass):
    folderdf = pd.read_excel('classes.xlsx',sheet_name='Folders')
    folderdf.index = folderdf.iloc[:,0]
    return folderdf.loc[nclass]

def get_class(wkd,tm):
    classdf = pd.read_excel('classes.xlsx',sheet_name='Classes')
    if tm in classdf.Time:
        print('Found!')
        classser = classdf.loc[:,wkd]
        nclass = classser[tm]
        return nclass
    else:
        return 0

def open_folder_scheduled():
    tm = strftime('%H:%M')
    wkd = strftime('%a')
    nclass = get_class(wkd,tm)
    if nclass:
        folder = get_folder(nclass)
        os.system('explorer '+folder)
        print('folder opened')

open_folder_scheduled()
