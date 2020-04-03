#!/usr/bin/env python
# -*- coding:utf-8 -*-
import cartinit
from math import atan
from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager, SlideTransition
from kivy.uix.gridlayout import GridLayout
from kivy.lang import Builder
from kivy.uix.widget import Widget
from clientbase.clientbase import ClientBase
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.clock import Clock
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

class At(Widget):
    angle = NumericProperty(0)
    last_x = 0
    last_y = 0
    def getangle(self):
        delta_x = self.center_x - self.last_x
        delta_y = self.center_y - self.last_y
        self.last_x = self.center_x
        self.last_y = self.center_y
        if(delta_x == 0 and delta_y >= 0):
            return 0.78539816325
        elif(delta_x == 0 and delta_y < 0):
            return 3.92699081625
        theta = atan(delta_y / delta_x)
        if(delta_x > 0):
            return theta - 0.78539816325
        else:
            return theta + 2.35619448975
    pass

class LeadScreen(DefaultScreen):
    at = ObjectProperty(None)
    def on_touch_move(self, touch):
        angle = self.at.getangle()
        self.at.center = touch.x, touch.y
        self.at.angle = float(angle)
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
        leadscreen = LeadScreen()
        screen = Screen(name = 'Lead')
        screen.add_widget(leadscreen)
        sm.add_widget(screen)
        return sm
if __name__ == '__main__':
    app = CartApp()
    app.run()
