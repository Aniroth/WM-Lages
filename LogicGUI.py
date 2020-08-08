"""PyQT imports"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QTableWidgetItem

"""GUI Drawners imports"""
from GUI.MainWindow.DrawMainWindow import Ui_MainWindow
from GUI.BuscarPedido.DrawBuscarPedido import Ui_DIALOG_BuscaPedido

from DataBase import *
from Objects import *

import sys

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setupConnections()
        self.dataBase = DataBaseConnection()

    def setupConnections(self):
        self.PBT_Salvar.clicked.connect(self.SalvarPedido)
        self.PBT_Buscar.clicked.connect(self.ShowBuscarPedido)

    def SalvarPedido(self):
        
        cabotagem = int(self.CHB_Cabotagem.isChecked())
        expurgo = int(self.CHB_Expurgo.isChecked())

        novoPedido = Pedido(self.TXB_Pedido.text(),
                            self.TXB_Booking.text(),
                            self.CBX_Status.currentText(),
                            cabotagem,
                            expurgo,
                            self.CBX_Armador.currentText(),
                            self.CBX_Fabrica.currentText(),
                            self.CBX_Porto.currentText(),
                            self.DATE_DL_Fabrica.text(),
                            self.DATE_DL_Porto.text(),
                            self.DATE_InicioJanela.text(),
                            self.DATE_FimJanela.text(),
                            None,
                            self.CBX_TerminalVazio.currentText())
        
        self.dataBase.SavePedido(novoPedido)
    
    def CarregarPedido(self, numeroPedido):
        return 'a'

    def ShowBuscarPedido(self):
        self.buscarPedidoDialog = BuscarPedidoDialog(self)
        self.buscarPedidoDialog.show()

class BuscarPedidoDialog(QtWidgets.QDialog, Ui_DIALOG_BuscaPedido):
    def __init__(self, _parentWindow, parent=None):
        super(BuscarPedidoDialog, self).__init__(parent)
        self.parentWindow = _parentWindow
        self.setupUi(self)
        self.setupConnections()
        self.dataBase = DataBaseConnection()
    
    def setupConnections(self):
        self.TXB_Busca.editingFinished.connect(self.FillTable)
        self.PBT_Selecionar.clicked.connect(self.SelecionarPedido)

    def FillTable(self):
        self.TABLE_BuscarPedido.clear()
        dataStream = self.dataBase.FillPedidoSearch(self.CHB_TipoBusca.currentText(),
                                                    self.TXB_Busca.text())

        if (dataStream == []):
            error_dialog = QtWidgets.QErrorMessage()
            error_dialog.showMessage('Oh no!')
            return

        self.TABLE_BuscarPedido.setRowCount(len(dataStream))
        self.TABLE_BuscarPedido.setColumnCount(len(dataStream[0]))

        for row in range(len(dataStream)):

            for col in range(len(dataStream[row])):

                self.TABLE_BuscarPedido.setItem(row, col, QTableWidgetItem(str(dataStream[row][col])))
    
    def SelecionarPedido(self):
        index = (self.TABLE_BuscarPedido.selectionModel().currentIndex())
        value = index.sibling(index.row(), index.column()).data()
        self.parentWindow.CarregarPedido(value)
        print(value)
        self.destroy()
