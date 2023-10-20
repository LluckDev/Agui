from tkinter import *
from PIL import Image,ImageTk

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
        self.runningPointer = id(self.running)
        self.mx = 0
        self.my = 0
        self.mousepressed = False
        self.keypressed = False
        self.mousePressedFunc = None
        self.keyPressedFunc = None
        self.winx = self.window.winfo_width()
        self.winy = self.window.winfo_height()
        self.lastKey = " "

        # Internal vars["image",tag,x,y,sx,sy,image,imageI]
        self.hs = {True: "normal", False: "hidden"}
        self.lineI = {"x": 2, "y": 3, "xp": 4, "yp": 5, "fill": 6, "stroke": 7, "visible": 8}
        self.TextI = {"x": 2, "y": 3, "size": 4, "text": 5, "fill": 6, "angle": 7, "visible": 8}
        self.hitbloxI = {"x": 2, "y": 3, "xp": 4, "yp": 5, "func": 6, "on": 7}
        self.mouseoverI = {"x": 2, "y": 3, "xp": 4, "yp": 5,"OnFunc":6,"OffFunc":7,"on":8}
        self.triI = {"x": 2, "y": 3, "xp": 4, "yp": 5, "xpp": 6, "ypp": 7, "fill": 8, "stroke": 9, "visible": 10}
        self.imageI = {"x":2,"y":3,"sx":4,"sy":5,"image":6,"imageI":7}

        # protocols
        self.window.protocol("WM_DELETE_WINDOW", self.__close__)
        self.window.bind("<Configure>", self.__OnResize__)
        self.canvas.bind("<Button-1>", self.__mousePressed__)
        self.window.bind("<Key>", self.__keypressed__)

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
        if self.mousePressedFunc != None:
            self.mousePressedFunc()
    def __keypressed__(self,i):
        self.lastKey = i.char
        self.keypressed = True
        if self.keyPressedFunc != None:
            self.keyPressedFunc(i.char)

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
        self.keypressed = True

        # actual updating window back end
        # at end
        self.window.update_idletasks()
        self.window.update()

    def activeUpdate(self):
        for i in range(len(self.active)):
            if self.data[self.active[i]][0] == "hitbox" and self.data[self.active[i]][7]:
                self.UPDATEhitbox(self.active[i])
            if self.data[self.active[i]][0] == "mouseover" and self.data[self.active[i]][8]:
                self.UPDATEmouseover(self.active[i])

    def UPDATEhitbox(self, i):
        if inArea(self.data[i][2], self.data[i][3], self.data[i][4], self.data[i][5], self.mx,
                  self.my) and self.mousepressed:
            self.data[i][6]()

    def UPDATEmouseover(self, i):
        if inArea(self.data[i][2], self.data[i][3], self.data[i][4], self.data[i][5], self.mx, self.my):
            if not (self.data[i][9]):
                self.data[i][6]()
                self.data[i][9] = True
        else:
            if self.data[i][9]:
                self.data[i][7]()
                self.data[i][9] = False

    # base widgets
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
        self.data.append(["Rect", tag, x, y, xp, yp, fill, stroke, visable])
        self.numb += 1
        if not (visable):
            self.canvas.itemconfig(self.objects[tag], state="hidden")

    def tri(self,tag,x,y,xp,yp,xpp,ypp,fill="#ffffff",stroke="#000000",visible=True):
        self.objects[tag] = self.canvas.create_polygon(x,y,xp,yp,xpp,ypp,fill=fill,outline=stroke)
        self.location[tag] = self.numb
        self.numb += 1
        self.data.append(["tri",tag,x,y,xp,yp,xpp,ypp,fill,stroke,visible])
        if not (visible):
            self.canvas.itemconfig(self.objects[tag], state="hidden")

    def text(self, tag, x, y, size=10, text: str = "none", fill="#000000", visable=True, angle=0):
        self.objects[tag] = self.canvas.create_text(x, y, text=text, fill=fill, angle=angle)
        self.location[tag] = self.numb
        self.data.append(["Text", tag, x, y, size, text, fill, angle, visable])
        self.numb += 1
        if not (visable):
            self.canvas.itemconfig(self.objects[tag], state="hidden")

    # mouse wigets
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

    def image(self,tag,x,y,sx="d",sy="d",image="files/Agui.png",visible=True):
        imageI = Image.open(str(image))
        if sx != "d" and sy != "d":
            imageI = imageI.resize((sx,sy))
        imageI = ImageTk.PhotoImage(imageI)

        self.data.append(["image",tag,x,y,sx,sy,image,imageI])
        self.objects[tag]=self.canvas.create_image(x,y,anchor=NW,image=self.data[self.numb][7])
        del imageI
        self.numb +=1

    # updating code
    def updateType(self, tag, item, value):

        type = self.data[self.location[tag]][0]
        i = self.location[tag]
        if type == "line":
            try:
                self.data[i][self.lineI[item]] = value
                self.canvas.coords(self.objects[tag], self.data[i][2], self.data[i][3], self.data[i][4],
                                   self.data[i][5])
                self.canvas.itemconfig(self.objects[tag], fill=self.data[i][7], state=self.hs[self.data[i][8]])
            except:
                raise Exception("Incorrect Item Value \nuse: x,y,xp,yp,stroke,visible")
        if type == "Rect":
            try:
                self.data[i][self.lineI[item]] = value
                self.canvas.coords(self.objects[tag], self.data[i][2], self.data[i][3], self.data[i][4],
                                   self.data[i][5])
                self.canvas.itemconfig(self.objects[tag], fill=self.data[i][6], outline=self.data[i][7],
                                       state=self.hs[self.data[i][8]])
            except:
                raise Exception("Incorrect Item Value \nuse: x,y,xp,yp,fill,stroke,visible")
        if type == "Text":
            try:
                self.data[i][self.TextI[item]] = value
                self.canvas.coords(self.objects[tag], self.data[i][2], self.data[i][3])
                self.canvas.itemconfig(self.objects[tag], fill=self.data[i][6], angle=self.data[i][7],
                                       state=self.hs[self.data[i][8]])
            except:
                raise Exception("Incorrect Item Value \nuse: x,y,size,text,fil,angle,visible")
        if type == "hitbox":
            try:
                self.data[i][self.hitboxI[item]] = value
            except:
                raise Exception("Incorrect Item Value \nuse: x,y,xp,yp,func,on")
        if type == "mouseover":
            try:
                self.data[i][self.mouseoverI[item]] = value
            except:
                raise Exception("Incorrect Item Value \nuse: x,y,xp,yp,OnFunc,OffFunc,on")
        if type == "tri":
            try:
                self.data[i][self.triI[item]] = value
                self.canvas.coords(self.objects[tag], self.data[i][2], self.data[i][3], self.data[i][4],
                                   self.data[i][5],self.data[i][6],self.data[i][7])
                self.canvas.itemconfig(self.objects[tag], fill=self.data[i][8], outline=self.data[i][9],
                                       state=self.hs[self.data[i][10]])
            except:
                raise Exception("Incorrect Item Value \nuse: x,y,xp,yp,xpp,ypp,fill,stroke,visible")

    def get(self,tag,item):
        type = self.data[self.location[tag]][0]
        i = self.location[tag]

        if type == "line":
            return self.data[i][self.lineI[item]]
        if type == "Rect":
            return self.data[i][self.lineI[item]]
        if type == "Text":
            return self.data[i][self.TextI[item]]
        if type == "hitbox":
            return self.data[i][self.hitbloxI[item]]
        if type == "mouseover":
            return self.data[i][self.mouseoverI[item]]
        if type == "tri":
            return self.data[i][self.triI[item]]
        if type == "image":
            return self.data[i][self.imageI[item]]

