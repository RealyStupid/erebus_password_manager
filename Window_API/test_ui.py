# Import everything from tkinter
from tkinter import *

# Widgets = GUI elements: buttons, textboxes, labels, images
# windows = serves as a container to hold or contain these widgets
# label = an area widjet that holds text and/or an image within a window

window = Tk() # instantiate an instance of a window

window.geometry("1000x1000") # set initial size of window
# window.resizable(False, False) force whether i want the window to change its geomatry (ig if i want to lock the x, y or both)
window.title("epic first GUI") # set the name of the window

#Icon creation and setting
# icon = PhotoImage(file="image dir")
# window.iconphoto(True, icon)

window.config(background="gray") #config allows me to change properites

# create a label, but wont show on the window yet
label = Label(
    window, 
    text="Epic text", 
    font=("Arial", 40, 'bold'), 
    fg="green", bg="gray",
    relief=RAISED,
    bd=20,
    padx=30,
    pady=50
   )
label.pack() # now this added the label to the window at the center
#label.place(x=100,y=200) # this places the text at a specific cords
# both of these create a background on the text

window.mainloop() # Place window on screen, listens for events