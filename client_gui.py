# -*- coding: utf-8 -*-
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

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
import os
from multiprocessing import Process
from rand_select import rand_sample

def system_call(wd):
    os.system('cd {} && activate ML && python recognition.py'.format(wd))


class Client(App):
    theme_cls = ThemeManager()
    title = 'Intelligent Teaching Client'

    def build(self):
        kv = Builder.load_file('main_frame.kv')
        return kv
    
    def show_snackbar(self):
        Snackbar(text="This is a program designed for intelligent teaching!\nVersion 0.1\nMade by: Skymos, Jiao Shixuan").show()

    def start_process(self):
        self.root.ids.statuslabel.text = 'Please wait.Loading the model and starting the process.'
        p = Process(target=system_call,args=(os.getcwd(),))
        p.start()
        p.join()
    def random_select(self):
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

if __name__     == '__main__':
    client = Client()
    client.run()