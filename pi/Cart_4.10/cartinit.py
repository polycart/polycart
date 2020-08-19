"""
    Initialize the application.
"""

# change working directory to the containing directory of main.py
import os, sys

os.chdir(sys.path[0])

# check kv version
import kivy
from kivy.config import Config


def init():
    kivy.require('1.11.1')

    # config cursor and fullscreen, also can be write in config.ini
    Config.set('graphics', 'width', 800)
    Config.set('graphics', 'height', 480)
#    Config.set('graphics', 'fullscreen', 0)
    Config.set('graphics', 'show_cursor', 1)
    Config.set('graphics', 'maxfps', 24)
    Config.set('kivy', 'log_level', 'trace')
    Config.write()
