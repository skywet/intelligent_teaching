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
from kivymd.list import MDList
from kivymd.list import ILeftBody, ILeftBodyTouch, IRightBodyTouch, BaseListItem
from kivymd.material_resources import DEVICE_TYPE
from kivymd.navigationdrawer import MDNavigationDrawer, NavigationDrawerHeaderBase
from kivymd.selectioncontrols import MDCheckbox
from kivymd.snackbar import Snackbar
from kivymd.theming import ThemeManager
from kivymd.grid import SmartTile
from kivymd.time_picker import MDTimePicker
from kivymd.list import OneLineListItem
import os
from multiprocessing import Process
from rand_select import rand_sample,load_y
import webbrowser

def system_call(wd):
    os.system('cd {} && activate ML && python recognition.py'.format(wd))


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

    def start_process(self):
        '''
        启动识别进程
        '''
        self.root.ids.statuslabel.text = 'Please wait.Loading the model and starting the process.'
        p = Process(target=system_call,args=(os.getcwd(),))
        p.start()
        p.join()
    
    '''
    def show_student_screen(self):
    '''

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

    def open_dash(self,people):
        '''
        启动dash，原因不明为何要写成包装函数的样式
        '''
        def init(self):
            url = people
            webbrowser.open(url)
        return init
            

    def open_lead_list(self,**kwargs):
        try:
            self.root.ids.ml.clear_widgets()
        finally:
            self.root.ids.scr_mngr.current = 'studentlist'
            y = load_y()
            for people in y:
                item = OneLineListItem(text=people,on_release=self.open_dash(people))
                self.root.ids.ml.add_widget(item)
    
    def open_img(self,**kwargs):
        try:
            self.root.ids.dash.clear_widgets()
        finally:
            self.root.ids.scr_mngr.current = 'dash'
            for file in os.listdir('presence/plot'):
                item = SmartTile(mipmap=True,source='presence/plot/{}'.format(file))
                self.root.ids.dash.add_widget(item)

if __name__ == '__main__':
    client = Client()
    client.run()