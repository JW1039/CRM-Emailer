import tkinter as tk
import json
from Widgets import MenuBar, FilePicker
from os import path, getenv
from Config import Config


file_path = getenv("APPDATA") + "\Emailer\config.json"
if path.exists(file_path):
    with open(file_path) as json_file:
        config_file = json.load(json_file)
        global user_conf
        user_conf = Config(config_file)


def onDestroy():
    filepicker = FilePicker(window, user_conf, onDestroy)


WIDTH = 600
HEIGHT = 600

# COLOURS:
MAIN_BG = "#290769"

window = tk.Tk()
window.title("Emailer")
window.geometry("%sx%s" % (WIDTH,HEIGHT))


menubar = MenuBar(window)

filepicker = FilePicker(window, user_conf, onDestroy)


window.mainloop()


