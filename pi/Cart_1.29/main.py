#!/usr/bin/env python
# -*- coding:utf-8 -*-
import cartinit
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.widget import Widget
cartinit.init()

# create ScreenManager as root, put all screens into
sm = ScreenManager()
sm.transition = SlideTransition()
screens = []

# load kv files
Builder.load_file('screens.kv')
class DefaultGridLayout(GridLayout):
	# DefaultGridLayout, default the size or other properties
	pass

class DefaultScreen(Widget):
    # DefaultScreen, other screen should be subclass of DefaultScreen
    pass


class MainScreen(DefaultScreen):

    # main menu on startup
    pass


class CartApp(App):
    # main app
    def build(self):
        mainscreen = MainScreen()
        screen = Screen(name = 'Menu')
        screen.add_widget(mainscreen)
        sm.add_widget(screen)
        return sm
if __name__ == '__main__':
    app = CartApp()
    app.run()
