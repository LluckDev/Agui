from tkinter import *


# common fucncs
def inArea(x, y, xp, yp, mx, my):
    if x <= mx <= xp and y <= my <= yp:
        return True
    else:
        return False




#main class

class Window:

    def __init__(self, grid=100, screenX=800, screenY=520, bgc="#ffffff", fullscreen=False,title="My Amazing Gui"):

        # object storage
        self.objects = {}  # dict
        self.location = {}  # dict
        self.data = []  # array


        # setup screen
        self.window = Tk()
        self.window.geometry(str(screenX) + "x" + str(screenY))
        self.window.columnconfigure(100, weight=100)
        self.window.title(title)
        self.window.rowconfigure(100, weight=100)
        self.canvas = Canvas(self.window, width=self.window.winfo_width() / 1.25,
                             height=self.window.winfo_height() / 1.25, bg=bgc)
        if fullscreen == True:
            self.window.state('zoomed')
        self.canvas.grid(row=1)
        self.i = grid


        #vars
        self.running = True


        #protocols
        self.window.protocol("WM_DELETE_WINDOW", self.__close__)


    def __close__(self):
        self.running = False
    def update(self):


        # actual updating window back end
        # at end
        self.window.update_idletasks()
        self.window.update()

