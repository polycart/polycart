"""
    Initialize the application.
"""

# change working directory to the containing directory of main.py
import os, sys

os.chdir(sys.path[0])

# check kv version
import kivy

kivy.require('1.11.1')

# config cursor and fullscreen, also can be write in config.ini
from kivy.config import Config

Config.set('graphics', 'fullscreen', 'auto')
Config.set('graphics', 'show_cursor', False)
Config.write()
