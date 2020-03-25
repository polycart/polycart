#!/usr/bin/env python
# -*- coding:utf-8 -*-
import cartinit
from math import atan, fabs
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
            self.result.text = "[color=ff0000]*连接错误*[/color]"
        pass
    def newuser(self):
        res = client.NewUser(self.username, self.password)
        if(res):
            self.result.text = "[color=00ff00]*注册成功*[/color]"
        else:
            self.result.text = "[color=ff0000]*注册失败*[/color]"
    def login(self):
        res = client.LogIn(self.username, self.password)
        if(res):
            self.result.text = "[color=00ff00]*登录成功*[/color]"
        else:
            self.result.text = "[color=ff0000]*登录失败*[/color]"
    def back(self):
        sm.current = 'Menu'
    pass

class LoggedScreen(DefaultScreen):
    def back(self):
        sm.current = 'Menu'
    pass

class At(Widget):
    angle = NumericProperty(0)
    show_direction = NumericProperty(0)
    last_x = 0
    last_y = 0
    def getangle(self):
        delta_x = self.center_x - self.last_x
        delta_y = self.center_y - self.last_y
        self.last_x = self.center_x
        self.last_y = self.center_y
        if(delta_x * delta_x + delta_y * delta_y < 5):
            self.show_direction = 0
            return 45
        self.show_direction = 1
        if(delta_x == 0 and delta_y >= 0):
            return 45
        elif(delta_x == 0 and delta_y < 0):
            return 225
        theta = atan(delta_y / delta_x)
        if(delta_x > 0):
            return (theta * 57.29577952383886) - 45
        else:
            return (theta * 57.29577952383886) + 135
    def update(self, dt):
        angle = self.getangle()
        self.angle = angle
    pass

class LeadScreen(DefaultScreen):
    at = ObjectProperty(None)
    scroll = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        Clock.schedule_interval(self.at.update, 0.5)
    def on_touch_move(self, touch):
        if(fabs(touch.x - self.width * 0.3) < 210 and fabs(touch.y - self.height * 0.45) < 190):
            self.at.center = touch.x, touch.y
    def search(self):
        self.scroll.remove()
        print(self.scroll.siz)
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
