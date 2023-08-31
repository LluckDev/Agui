from tkinter import *


# common fucncs
def inArea(x, y, xp, yp, mx, my):
    if x <= mx <= xp and y <= my <= yp:
        return True
    else:
        return False


# main class
class Window:
    def __init__(self, grid=100, screenX=800, screenY=520, bgc="#ffffff", fullscreen=False, title="My Amazing Gui"):
        # object storage
        self.objects = {}  # dict
        self.location = {}  # dict
        self.active = []  # aray
        self.data = []  # array
        self.numb = 0  # amount of items in list

        # setup screen
        self.window = Tk()
        self.window.configure(bg=bgc)
        self.window.geometry(str(screenX) + "x" + str(screenY))
        self.window.title(title)
        self.canvas = Canvas(self.window, width=self.window.winfo_width() / 1.25,
                             height=self.window.winfo_height() / 1.25, bg=bgc)
        if fullscreen:
            self.window.state('zoomed')
        self.canvas.pack()
        self.i = grid

        # vars
        self.running = True
        self.mx = 0
        self.my = 0
        self.mousepressed = False

        self.winx = self.window.winfo_width()
        self.winy = self.window.winfo_height()

        # protocols
        self.window.protocol("WM_DELETE_WINDOW", self.__close__)
        self.window.bind("<Configure>", self.__OnResize__)
        self.canvas.bind("<Button-1>", self.__mousePressed__)

        # themes
        self.theme = []
        self.themes = [["#2d2d30", "#363638", "#787879", "#ebebeb", "#2093fe", "#2b3744"]]
        # [back,mid,front,text,highlight,highlight back]

    def __close__(self):
        self.running = False

    def __OnResize__(self, event):
        self.window.config(width=event.width, height=event.height)
        self.winx = self.window.winfo_width()
        self.winy = self.window.winfo_height()
        self.canvas.config(width=self.winx + 20, height=self.winy + 20)

    def __mousePressed__(self, i):
        self.mousepressed = True

    def update(self):
        # update vars
        # FIRST

        self.mx = self.window.winfo_pointerx()
        self.mx -= self.window.winfo_x()
        self.my = self.window.winfo_pointery()
        self.my -= self.window.winfo_x()
        self.my -= 30

        # updates

        self.activeUpdate()

        # close one ticks
        self.mousepressed = False

        # actual updating window back end
        # at end
        self.window.update_idletasks()
        self.window.update()

    def activeUpdate(self):
        for i in range(len(self.active)):
            if self.data[self.active[i]][0] == "hitbox" and self.data[self.active[i]][7]:
                self.UPDATEhitbox(self.active[i])
            if self.data[self.active[i]][0] == "mouseover"  and self.data[self.active[i]][8]:
                self.UPDATEmouseover(self.active[i])

    def UPDATEhitbox(self, i):
        if inArea(self.data[i][2], self.data[i][3], self.data[i][4], self.data[i][5], self.mx,
                  self.my) and self.mousepressed:
            self.data[i][6]()

    def UPDATEmouseover(self, i):
        if inArea(self.data[i][2], self.data[i][3], self.data[i][4], self.data[i][5], self.mx, self.my):
            if not(self.data[i][9]):
                self.data[i][6]()
                self.data[i][9] = True
        else:
            if self.data[i][9]:
                self.data[i][7]()
                self.data[i][9] = False

    def line(self, tag, x, y, xp, yp, stroke="#000000", visable=True):
        self.objects[tag] = self.canvas.create_line(x, y, xp, yp, fill=stroke)
        self.location[tag] = self.numb
        self.data.append(["line", tag, x, y, xp, yp, None, stroke, visable])
        self.numb += 1
        if not (visable):
            self.canvas.itemconfig(self.objects[tag], state="hidden")

    def rect(self, tag, x, y, xp, yp, fill="#ffffff", stroke="#000000", visable=True):
        self.objects[tag] = self.canvas.create_rectangle(x, y, xp, yp, fill=fill, outline=stroke)
        self.location[tag] = self.numb
        self.data.append(["line", tag, x, y, xp, yp, fill, stroke, visable])
        self.numb += 1
        if not (visable):
            self.canvas.itemconfig(self.objects[tag], state="hidden")

    def text(self, tag, x, y, size=10, text: str = "none", fill="#000000", visable=True, angle=0):
        self.objects[tag] = self.canvas.create_text(x, y, text=text, fill=fill, angle=angle)
        self.location[tag] = self.numb
        self.data.append(["line", tag, x, y, size, text, fill, angle, visable])
        self.numb += 1
        if not (visable):
            self.canvas.itemconfig(self.objects[tag], state="hidden")

    def hitbox(self, tag, x, y, xp, yp, func, on=True):
        self.active.append(self.numb)
        self.location[tag] = self.numb
        self.data.append(["hitbox", tag, x, y, xp, yp, func, on])
        self.numb += 1

    def mouseover(self, tag, x, y, xp, yp, OnFunc, OffFunc, on=True):
        self.active.append(self.numb)
        self.location[tag] = self.numb
        self.data.append(["mouseover", tag, x, y, xp, yp, OnFunc, OffFunc, on, False])
        self.numb += 1
