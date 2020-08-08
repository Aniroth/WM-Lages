"""PyQT imports"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication

"""GUI Drawners imports"""
from GUI.MainWindow.DrawMainWindow import Ui_MainWindow

from DataBase import *
from Objects import *

import sys

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setupConnections(self)
        self.dataBase = DataBaseConnection()

    def setupConnections(self, MainWindow):
        MainWindow.PBT_Salvar.clicked.connect(lambda: self.SalvarPedido(MainWindow))

    def SalvarPedido(self, MainWindow):
        
        if (MainWindow.CHB_Cabotagem.isChecked()):
            cabotagem = 1
        else:
            cabotagem = 0
        
        if (MainWindow.CHB_Expurgo.isChecked()):
            expurgo = 1
        else:
            expurgo = 0


        novoPedido = Pedido(MainWindow.TXB_Pedido.text(),
                            MainWindow.TXB_Booking.text(),
                            MainWindow.CBX_Status.currentText(),
                            cabotagem,
                            expurgo,
                            MainWindow.CBX_Armador.currentText(),
                            MainWindow.CBX_Fabrica.currentText(),
                            MainWindow.CBX_Porto.currentText(),
                            MainWindow.DATE_DL_Fabrica.text(),
                            MainWindow.DATE_DL_Porto.text())
        
        self.dataBase.SavePedido(novoPedido)