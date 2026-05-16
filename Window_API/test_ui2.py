#more practical test

from tkinter import *

# window shi
window = Tk() # instance a window
# Anything within/before main loop will be the eliments
window.geometry("600x700") # set the size of window
window.title("Another test") # set the window title
window.resizable(width=False, height=False) #can force a width or height

tital = Label(
    window,
    text="EREBUS PASSWORD MANAGER",
    font=('Arial', 20, 'bold')
)

tital.pack()

window.mainloop() # display window