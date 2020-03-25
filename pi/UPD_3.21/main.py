#!/usr/bin/env python
# -*- coding:utf-8 -*-
import cartinit
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.widget import Widget
from clientbase.clientbase import ClientBase
from kivy.properties import StringProperty, ObjectProperty
client = ClientBase()
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
    def move_to(self, name):
        sm.current = name
    # main menu on startup
    pass

class LoginScreen(DefaultScreen):
    result = ObjectProperty(None)
    username = StringProperty("")
    password = StringProperty("")
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if client.clisock.state != 'Connected':
            self.result.text = "[color=ff0000]Connect Error[/color]"
        pass
    def newuser(self):
        res = client.NewUser(self.username, self.password)
        self.result.text = str(res)
    def login(self):
        res = client.LogIn(self.username, self.password)
        self.result.text = str(res)
    def back(self):
        sm.current = 'Menu'
    pass

class LoggedScreen(DefaultScreen):
    def back(self):
        sm.current = 'Menu'
    pass

class CartApp(App):
    # main app
    def build(self):
        mainscreen = MainScreen()
        screen = Screen(name = 'Menu')
        screen.add_widget(mainscreen)
        sm.add_widget(screen)
        loginscreen = LoginScreen()
        screen = Screen(name = 'Login')
        screen.add_widget(loginscreen)
        sm.add_widget(screen)
        loggedscreen = LoggedScreen()
        screen = Screen(name = 'Logged')
        screen.add_widget(loggedscreen)
        sm.add_widget(screen)
        return sm
if __name__ == '__main__':
    app = CartApp()
    app.run()
