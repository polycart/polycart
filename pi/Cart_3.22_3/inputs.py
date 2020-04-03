from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.lang import Builder
from kivy.properties import StringProperty

Builder.load_file('inputs.kv')

class LabelInput(GridLayout):
	title = StringProperty('title')
	text = StringProperty('text')
	pass
