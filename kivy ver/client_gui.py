# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen
from kivy.utils import get_color_from_hex
from kivy.config import Config

from kivymd.color_definitions import colors 
from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton,MDFloatingActionButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import MDList
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.grid import SmartTile,SmartTileWithLabel
from kivymd.time_picker import MDTimePicker
from kivymd.list import OneLineListItem

import os
from multiprocessing import Process
from rand_select import rand_sample,load_y
import webbrowser
import pandas as pd
from time import strftime
from warning_module import warning

def system_call(wd):
    os.system('cd {} && activate ML && python recognition.py'.format(wd))

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

class Client(App):
    icon = 'icon.ico'
    theme_cls = ThemeManager()
    title = 'Intelligent Teaching Client'

    def build(self):
        self.icon = 'icon.ico'
        kv = Builder.load_file('main_frame.kv')
        return kv
    
    def show_snackbar(self):
        '''
        弹出提示信息
        '''
        Snackbar(text="This is a program designed for intelligent teaching!\nVersion 0.1\nMade by: Skymos, Jiao Shixuan").show()

    def warning_label(self):
        with open('config.ini') as cfg:
            lines = cfg.readlines()
            open_folder = bool(lines[0].split('=')[1])
            tolerence = int(lines[1].split('=')[1])
        warnlst = warning(tolerence)[1]
        st = '\n'.join(warnlst)
        self.root.ids.warning.text = "The following students will fail to get their score if they are late for another time\n"+st
    
    def start_process(self):
        '''
        启动识别进程
        '''
        self.root.ids.statuslabel.text = 'Please wait.Loading the model and starting the process.'
        p = Process(target=system_call,args=(os.getcwd(),))
        p.start()
        p.join()
    
    def random_select(self):
        '''
        弹出随机选择的人的ID
        '''
        num = int(self.root.ids.num_slider.value)
        st = rand_sample(num)
        content = MDLabel(font_style='Body1',
                          theme_text_color='Secondary',
                          text=st,
                          size_hint_y=None,
                          valign='top')
        content.bind(texture_size=content.setter('size'))
        self.dialog = MDDialog(title="Student selected:",
                               content=content,
                               size_hint=(.8, None),
                               height=dp(200),
                               auto_dismiss=False)

        self.dialog.add_action_button("Dismiss",
                                      action=lambda *x: self.dialog.dismiss())
        self.dialog.open()

    
    def open_img(self,**kwargs):
        try:
            self.root.ids.dash.clear_widgets()
        finally:
            self.root.ids.scr_mngr.current = 'dash'
            for file in os.listdir('presence/plot'):
                item = SmartTile(mipmap=True,source='presence/plot/{}'.format(file))
                self.root.ids.dash.add_widget(item)

def run():
    client = Client()
    client.run()

if __name__ == '__main__':
    with open('config.ini') as cfg:
        lines = cfg.readlines()
        open_folder = eval(lines[0].split('=')[1])
        tolerence = lines[1].split('=')[1]
    p1 = Process(target=run)
    if open_folder:
        p2 = Process(target=open_folder_scheduled)
        p2.daemon = True
        p2.start()
        print('Detecting process started')
    p1.start()
    p1.join()
    if open_folder:
        p2.join()