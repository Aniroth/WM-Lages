from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from GUI.MainWindow import Ui_MainWindow
import sys

class WMLagesApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(WMLagesApp, self).__init__(parent)
        self.setupUi(self)
        self.setupConnections(self)

    def setupConnections(self, MainWindow):
        MainWindow.PBT_Novo.clicked.connect(self.ClickTeste)
    
    def ClickTeste(self):
        print("TESTE")

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    form = WMLagesApp()
    form.showMaximized()
    app.exec_()

if __name__ == '__main__':
    main()