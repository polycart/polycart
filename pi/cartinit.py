"""
    Initialize the application.
"""

# change working directory to the containing directory of main.py
import os, sys

os.chdir(sys.path[0])

# check kv version
import kivy
from kivy.config import Config
from kivy.resources import resource_add_path


def init():
    kivy.require('1.11.1')

    # config cursor and fullscreen, also can be write in config.ini
    Config.set('graphics', 'fullscreen', 'auto')
    Config.set('graphics', 'show_cursor', False)
    Config.set('graphics', 'maxfps', 24)
    Config.write()

    # add resources path
    resource_add_path('./fonts/')
