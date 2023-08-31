from Agui import *





def start():
    window = Window(bgc="#444444")
    window.line("line",20,20,400,400)
    window.rect("rect",20,30,300,300)
    window.hitbox("hit",20,20,300,300,func=duck,on=False)
    window.mouseover("hof",20,20,300,300,OnFunc=duck1,OffFunc=you)
    window.text("str",140,140,text="suk a duck")

    while window.running:
        window.update()


def duck():
    print("duck")
def duck1():
    print("duck1")
def you():
    print("you")

if __name__ == '__main__':
    start()

