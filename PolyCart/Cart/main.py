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
from kivy.uix.bubble import Bubble
import time
from cv_detection import Detection
from location import Location
from weight import Weight
detection = Detection.get_instance()
detection.init()
client = ClientBase()
cartinit.init()
cart_pos = (0,0)

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

class GoodsListScreen(DefaultScreen):
    scroll = ObjectProperty(None)
    total_price = NumericProperty(0)
    total_weight = NumericProperty(0)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.payable = 0
    def refresh(self):
        goodslist = detection.get_commodities()
        self.scroll.remove()
        self.total_price = 0
        self.total_weight = 0
        if goodslist == None:
            self.scroll.add_info('http://39.96.48.80/error.png', '获取商品列表错误\n已申请人工介入', (0, 0))
            self.manualintervention()
            return
        goods_info = []
        for id in goodslist:
            num = goodslist[id]
            goods = client.GetGoodsById(str(id))
            time.sleep(0.1)
            if goods == False:
                continue
            goods_info.append(goods)
            self.total_price += float(goods[3]) * num
            self.total_weight += float(goods[7]) * num
        if self.weight_check() == 0:
            self.scroll.add_info('http://39.96.48.80/error.png', '重量错误,请重试\n多次错误请申请人工介入', (0, 0))
            self.payable = 0
        else:
            self.payable = 1
        for goods in goods_info:
            self.scroll.add_info('http://39.96.48.80/' + str(goods[2]), str(goods[1]) + '\n[' + str(num) + 'X]' + '￥' + str(goods[3]), (goods[4], goods[5]))
        self.scroll.scroll_y = 1
        sm.get_screen('Pay').children[0].setTotalPrice('￥' + ("%.2f" % self.total_price))

    def weight_check(self):
        weight = Weight.get_weight()
        if fabs(weight - self.total_weight) > 10:
            return False
        else:
            return True

    def manualintervention(self):
    	client.RequestMmanualIntervention(cart_pos)
    	self.move_to('Menu')

    def back(self):
        sm.current = 'Menu'
    def show(self, pos, img, name):
        pass
    def move_to(self, name):
        if self.payable:
            sm.current = name
	
	
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

class MoreInfo(Bubble):
    text = StringProperty('')
    img = StringProperty('')
    pass

class Point(Widget):
    img = StringProperty('')
    name = StringProperty('')
    info = ObjectProperty(None)
    def __init__(self, pos, img, name, **kwargs):
        super().__init__(**kwargs)
        self.center = pos
        self.img = img
        self.name = name
    def showinfo(self):
        if self.info.center_x > 1000:
            self.info.center_x -= 1000
            if self.info.x < 0:
                self.info.arrow_pos = 'bottom_left'
                self.info.center_x += self.info.width * 0.335
    

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
    name = ObjectProperty(None)
    at = ObjectProperty(None)
    scroll = ObjectProperty(None)
    the_map = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for one in client.ads:
            self.scroll.add_ad_lead('http://39.96.48.80/' + one[1], one[0], (one[2], one[3]))
        Clock.schedule_interval(self.at.update, 0.5)
        Clock.schedule_interval(self.update_at, 0.25)

    def update_at(self, dt):
        global cart_pos
        pos1 = Location.get_pos()
        pos2 = Location.get_pos()
        pos3 = Location.get_pos()
        if pos1 == None or pos2 == None or pos3 ==None:
            client.RequestMmanualIntervention(cart_pos)
            return
        pos = [0, 0]
        pos[0] = (pos1[0] + pos2[0] + pos3[0]) / 3
        pos[1] = (pos1[1] + pos2[1] + pos3[1]) / 3
        cart_pos = (pos[0], pos[1])
        self.at.center = self.the_map.x + pos[0] * 420 / 4, self.the_map.y + pos[1] * 380 / 5
        pass
    
    def search(self):
        if self.name.text == '':
            return

        self.scroll.remove()
        goodslist = client.SearchForGoods(self.name.text)
        for ones in goodslist:
            self.scroll.add_info('http://39.96.48.80/' + ones[1], ones[0] + '\n￥' + str(ones[2]), (ones[3], ones[4]))
    def show(self, pos, img, name):
        point = Point((self.the_map.pos[0] + pos[0], self.the_map.pos[1] + pos[1]), img, name)
        point.showinfo()
        self.add_widget(point)
        
    def show_ad_pos(self, pos, img, name):
        point = Point((self.the_map.pos[0] + pos[0], self.the_map.pos[1] + pos[1]), img, name)
        point.info.pic_hint = 0.3
        point.showinfo() 
        self.add_widget(point)

    def back(self):
        sm.current = 'Menu'
    pass

class AdScreen(DefaultScreen):
    scroll = ObjectProperty(None)
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for one in client.ads:
            self.scroll.add_ad('http://39.96.48.80/' + one[1], one[0], (one[2], one[3]))
    def show_ad_pos(self, pos, img, name):
        sm.current = 'Lead'
        sm.get_screen('Lead').children[0].show_ad_pos(pos, img, name)
    def back(self):
        sm.current = 'Menu'
    pass

class PayScreen(DefaultScreen):
	total_price = StringProperty("￥0.00")
	def back(self):
		sm.current = "List"
	def setTotalPrice(self, str):
		self.total_price = str
	pass

class CartApp(App):
    # main app
    def build(self):
        client.GetAds()
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
        adscreen = AdScreen()
        screen = Screen(name = 'Ads')
        screen.add_widget(adscreen)
        sm.add_widget(screen)
        payscreen = PayScreen()
        screen = Screen(name = 'Pay')
        screen.add_widget(payscreen)
        sm.add_widget(screen)
        goodslistscreen = GoodsListScreen()
        screen = Screen(name = 'List')
        screen.add_widget(goodslistscreen)
        sm.add_widget(screen)
        return sm
if __name__ == '__main__':
    app = CartApp()
    app.run()
