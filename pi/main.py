#!/usr/bin/python3

import cartinit
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.lang import Builder
from buttons import RoundedButton

# create ScreenManager as root, put all screens into
sm = ScreenManager()
sm.transition = SlideTransition()
screens = []

# load kv files
Builder.load_file('screens.kv')

class DefaultScreen(Screen):
    # DefaultScreen, other screen should be subclass of DefaultScreen
    pass

class MainScreen(DefaultScreen):
    # main menu on startup

class CartApp(App):
    # main app
    def build(self):
        return sm


if __name__ == '__main__':
    app = CartApp()
    screens.append(DefaultScreen())
    sm.switch_to(screens[-1])
    app.run()
