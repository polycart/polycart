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
	pass

class ScrollList(ScrollView):
	high = NumericProperty(58)
	layout = ObjectProperty(None)
	siz = NumericProperty(0)
	def add(self, image, text, pos):
		info = Infomation()
		info.image = image
		info.goodspos = pos
		info.text = text
		self.layout.add_widget(info)
		self.siz += 1
		pass
	def remove(self):
		self.layout.clear_widgets()
		self.siz = 0
		pass
	pass