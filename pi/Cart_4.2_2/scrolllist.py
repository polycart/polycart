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
		ad.pos = pos
		self.layout.add_widget(ad)
		self.layout.height += 185
	def remove(self):
		self.layout.clear_widgets()
		self.siz = 0
		pass
	pass