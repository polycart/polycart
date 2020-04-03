'''
Bubble
======

Test of the widget Bubble.
'''

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.button import Button
from kivy.lang import Builder
from kivy.uix.bubble import Bubble

Builder.load_string('''
<cut_copy_paste>
	arrow_pos: 'bottom_left'
    size_hint: (None, None)
    size: (240, 60)
    pos_hint: {'center_x': .5, 'y': .6}
    AsyncImage:
    	size_hint_x: 0.2
    	source: 'http://39.96.48.80/map.jpg'
    Label:
    	text: 'this is a label'
    	size_hint_x: 0.5
    GridLayout:
    	size_hint_x: 0.1
    	cols: 1
        BubbleButton:
    	    text: 'D'
    	BubbleButton:
    		text: 'X'
''')


class cut_copy_paste(Bubble):
    pass


class BubbleShowcase(FloatLayout):

    def __init__(self, **kwargs):
        super(BubbleShowcase, self).__init__(**kwargs)
        self.but_bubble = Button(text='Press to show bubble')
        self.but_bubble.bind(on_release=self.show_bubble)
        self.add_widget(self.but_bubble)

    def show_bubble(self, *l):
        if not hasattr(self, 'bubb'):
            self.bubb = bubb = cut_copy_paste()
            self.add_widget(bubb)


class TestBubbleApp(App):

    def build(self):
        return BubbleShowcase()


if __name__ == '__main__':
    TestBubbleApp().run()