from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from GUI.MainWindow.LogicMainWindow import Logic_MainWindow
import sys

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    form = Logic_MainWindow()
    form.showMaximized()
    app.exec_()

if __name__ == '__main__':
    main()