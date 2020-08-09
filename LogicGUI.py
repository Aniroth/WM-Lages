"""PyQT imports"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QTableWidgetItem

"""GUI Draw imports"""
from GUI.MainWindow.DrawMainWindow import Ui_MainWindow
from GUI.BuscarPedido.DrawBuscarPedido import Ui_DIALOG_BuscaPedido
from GUI.EditarCNTR.DrawEditarCNTR import Ui_DIALOG_EditarCNTR
from GUI.EditarViagem.DrawEditarViagem import Ui_DIALOG_EditarViagem

from DataBase import *
from Objects import *

import sys

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        self.setupConnections()
        self.dataBase = DataBaseConnection()
        self.NovoPedido()

    def setupConnections(self):
        self.PBT_Salvar.clicked.connect(self.SalvarPedido)
        self.PBT_Novo.clicked.connect(self.NovoPedido)
        self.PBT_Buscar.clicked.connect(self.ShowBuscarPedido)
        self.PBT_IncluirCNTR.clicked.connect(self.ShowEditarCNTR)

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
                            self.dataBase.GetCNTRs(self.TXB_Booking.text()),
                            self.CBX_TerminalVazio.currentText())
        
        self.dataBase.SavePedido(novoPedido)
    
    def CarregarPedido(self, _numeroPedido):
        datastream = self.dataBase.OpenPendido(str(_numeroPedido))
        self.TXB_Pedido.setText(str(datastream[0]))
        self.TXB_Booking.setText(str(datastream[2]))
        self.CBX_Status.setCurrentText(str(datastream[3]))
        self.CHB_Cabotagem.setChecked(bool(datastream[4]))
        self.CHB_Expurgo.setChecked(bool(datastream[5]))
        self.CBX_Armador.setCurrentText(str(datastream[6]))
        self.CBX_Fabrica.setCurrentText(str(datastream[7]))
        self.CBX_Porto.setCurrentText(str(datastream[8]))
        self.DATE_DL_Fabrica.setDate(self.GetDate(datastream[9]))
        self.DATE_DL_Porto.setDate(self.GetDate(datastream[10]))
        self.DATE_InicioJanela.setDate(self.GetDate(datastream[11]))
        self.DATE_FimJanela.setDate(self.GetDate(datastream[12]))
        self.CBX_TerminalVazio.setCurrentText(str(datastream[14]))
    
    def NovoPedido(self):
        today = QtCore.QDate.currentDate()
        self.TXB_Pedido.setText("")
        self.TXB_Booking.setText("")
        self.CBX_Status.currentIndex = 0
        self.CHB_Cabotagem.setChecked(False)
        self.CHB_Expurgo.setChecked(False)
        self.CBX_Armador.currentIndex = 0
        self.CBX_Fabrica.currentIndex = 0
        self.CBX_Porto.currentIndex = 0
        self.DATE_DL_Fabrica.setDate(today)
        self.DATE_DL_Porto.setDate(today)
        self.DATE_InicioJanela.setDate(today)
        self.DATE_FimJanela.setDate(today)
        self.CBX_TerminalVazio.currentIndex = 0

    def ShowBuscarPedido(self):
        self.buscarPedidoDialog = BuscarPedidoDialog(self)
        self.buscarPedidoDialog.show()

    def ShowEditarCNTR(self):
        self.editarCNTRDIalog = EditarCNTRDialog(self)
        self.editarCNTRDIalog.show()

    def GetDate(self, sTime):
        tempDate = str(sTime).split('/')
        date = QtCore.QDate(int(tempDate[2]), int(tempDate[1]), int(tempDate[0]))
        return date

class EditarCNTRDialog(QtWidgets.QDialog, Ui_DIALOG_EditarCNTR):
    def __init__(self, _parentWindow, parent = None):
        super(EditarCNTRDialog, self).__init__(parent)
        self.parentWindow = _parentWindow
        self.dataBase = DataBaseConnection()
        self.setupUi(self)
        self.setupConnections()
    
    def setupConnections(self):
        self.PBT_Gravar.clicked.connect(self.NovoCNTR)
        self.PBT_Cancelar.clicked.connect(self.Fechar)

    def NovoCNTR(self):
        
        novoCNTR = CNTR(
                        self.TXB_Unidade.text(),
                        self.CBX_Status.currentIndex(),
                        self.TXB_BKFantasma.text(),
                        self.SBX_Tara.text(),
                        self.TXB_BKReal.text()
                        )
        
        self.dataBase.SaveCNTR(novoCNTR)
        self.Fechar()
    
    def Fechar(self):

        self.hide()

class BuscarPedidoDialog(QtWidgets.QDialog, Ui_DIALOG_BuscaPedido):
    def __init__(self, _parentWindow, parent = None):
        super(BuscarPedidoDialog, self).__init__(parent)
        self.parentWindow = _parentWindow
        self.setupUi(self)
        self.setupConnections()
        self.dataBase = DataBaseConnection()
        self.FillTable()
    
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
        columnNames = ['Pedido', 'Booking', 'Status', 'DeadLine']
        self.TABLE_BuscarPedido.setHorizontalHeaderLabels(columnNames)

        for row in range(len(dataStream)):

            for col in range(len(dataStream[row])):

                self.TABLE_BuscarPedido.setItem(row, col, QTableWidgetItem(str(dataStream[row][col])))
    
    def SelecionarPedido(self):
        index = (self.TABLE_BuscarPedido.selectionModel().currentIndex())
        value = index.sibling(index.row(), 0).data()
        
        self.parentWindow.CarregarPedido(value)
        self.hide()
