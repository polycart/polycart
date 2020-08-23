from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.properties import StringProperty, ObjectProperty, NumericProperty
from kivy.lang import Builder

Builder.load_file('scrolllist.kv')
class Infomation(GridLayout):
	image = StringProperty('')
	text = StringProperty('')
	goods_pos = (0, 0)
	pass

class Advertisement(GridLayout):
	image = StringProperty('')
	text = StringProperty('')
	goods_pos = (0, 0)

	def on_touch_down(self, touch):
		if self.collide_point(touch.x, touch.y):
			self.parent.parent.parent.show_ad_pos(self.goods_pos, self.image, self.text)
	pass

class ScrollList(ScrollView):
	high = NumericProperty(58)
	layout = ObjectProperty(None)
	def add_info(self, image, text, pos):
		info = Infomation()
		info.image = image
		info.goodspos = pos
		info.text = text
		self.layout.add_widget(info)
		self.layout.height += 58
		pass

	def add_ad(self, image, text, pos):
		ad = Advertisement()
		ad.image = image
		ad.text = text
		ad.goods_pos = pos
		self.layout.add_widget(ad)
		self.layout.height += 360

	def add_ad_lead(self, image, text, pos):
		ad = Advertisement()
		ad.height = 180
		ad.image = image
		ad.text = text
		ad.goods_pos = pos
		self.layout.add_widget(ad)
		self.layout.height += 185
	def remove(self):
		self.layout.clear_widgets()
		self.layout.height = 0
		self.siz = 0
		pass
	pass