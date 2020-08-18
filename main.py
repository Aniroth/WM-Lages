from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5 import QtGui
from LogicGUI import MainWindow
from DataBase import DataBaseConnection

import sys
import os

VER = '2.56'

def launch():
    DataBaseConnection().UpdateDataBase()
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('fusion'))
    form = MainWindow()
    #form.showMaximized()
    app.exec_()
