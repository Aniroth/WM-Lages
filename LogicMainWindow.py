from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from GUI.MainWindow.DrawMainWindow import Ui_MainWindow
import sys

class Logic_MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Logic_MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setupConnections(self)

    def setupConnections(self, MainWindow):
        MainWindow.PBT_Salvar.clicked.connect(self.SalvarPedido)
    
    def SalvarPedido(self):
        print("TESTE")