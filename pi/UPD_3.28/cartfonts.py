"""
    Load font resources.
"""

from kivy.resources import resource_find, resource_add_path

resource_add_path('./fonts/')
titleFont = resource_find('title.ttf')
