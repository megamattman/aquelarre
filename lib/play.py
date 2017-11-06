from Tkinter import *

root = Tk()

root.wm_title("Kiosk")
root.geometry("300x75")
root.resizable(0, 0)

v=IntVar()
popcorn = Spinbox(root, from_=0, to=10, state="readonly", textvariable=v)
popcorn.pack()

def getvalue():
    print(v.get())
    setvalue()

def setvalue():
    v.set(0)

button = Button(root, text="Get value", command=getvalue)
button.pack()


root.mainloop()