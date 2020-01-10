#!/usr/bin/python3

import kivy
import sys, os
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.config import Config
from kivy.lang import Builder

kivy.require('1.11.1')

# change working directory to the containing directory of main.py
os.chdir(sys.path[0])

# config cursor and fullscreen, also can be write in config.ini
Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'show_cursor', False)
Config.write()

# create ScreenManager as root, put all screens into
sm = ScreenManager()
screens = []

# load kv files
Builder.load_file('cart.kv')


class DefaultScreen(Screen):
    # DefaultScreen类，用于派生子类
    pass


class CartApp(App):
    # main app
    def build(self):
        return sm


if __name__ == '__main__':
    app = CartApp()
    screens.append(DefaultScreen())
    sm.switch_to(screens[0])
    app.run()
