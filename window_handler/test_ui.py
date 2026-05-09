from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys


def window():
    # create the window
    app = QApplication(sys.argv)
    win = QMainWindow()

    #set position and size of window
    win.setGeometry(200, 200, 300, 300)

    #title of window
    win.setWindowTitle("test window")

    # contents inside the window
    label = QtWidgets.QLabel(win)
    label.setText("first label")
    label.move(50, 50)

    #run/display the window
    win.show()
    sys.exit(app.exec_())

window()