from Agui import *


def duck():
    print("duck")



def duck1():
    print("duck1")
    window.updateType("tri","xpp",90)
def you():
    print("you")
    window.updateType("rect","visible",True)



window = Window(bgc="#444444")
window.line("line",400,20,400,400)
window.rect("rect",20,30,300,300)
window.hitbox("hit",20,20,300,300,func=duck,on=False)
window.mouseover("hof",20,20,300,300,OnFunc=duck1,OffFunc=you)
window.text("str",140,140,text="suk a duck")
window.tri("tri",400,400,400,500,600,600)
window.image("img",300,300,200,100)
while window.running:
    window.update()





