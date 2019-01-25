# coding = utf-8
from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder

root = Builder.load_file('main.kv')

class MainApp(App):
    def build(self):
        return root

if __name__ == '__main__':
    MainApp().run()