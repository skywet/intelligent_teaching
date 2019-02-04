# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image

from kivymd.bottomsheet import MDListBottomSheet, MDGridBottomSheet
from kivymd.button import MDIconButton
from kivymd.date_picker import MDDatePicker
from kivymd.dialog import MDDialog
from kivymd.label import MDLabel
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.time_picker import MDTimePicker

class ConfigPanel(App):
    icon = 'icon.ico'
    theme_cls = ThemeManager()
    title = 'Config Panel'

    def build(self):
        kv = Builder.load_file('config.kv')
        return kv

    def load_config(self):
        try:
            with open('config.ini') as cfg:
                lines = cfg.readlines()
                open_folder = bool(lines[0].split('=')[1])
                freq = lines[1].split('=')[1]
            return (open_folder,freq)
        except FileNotFoundError:
            return (False,'4')
            
    def write_config(self):
        open_folder = self.root.ids.switch._active
        freq = self.root.ids.text.text
        with open('config.ini','w') as cfg:
            lines = ['open_folder={}'.format(open_folder),'freq={}'.format(freq)]
            cfg.writelines(lines)       
        return 1

if __name__ == '__main__':
    app = ConfigPanel()
    app.run()
   