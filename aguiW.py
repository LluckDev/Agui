from Agui import *

class Gui:
    def __init__(self,screenX=800, screenY=520, bgc="#ffffff", fullscreen=False, title="My Amazing Gui"):
        self.window = Window(screenX=screenX,screenY=screenY,bgc=bgc,fullscreen=fullscreen,title=title)
        self.running = self.window.running


    def update(self):
        self.window.update()
        self.running = self.window.running