"""PyQT imports"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QTableWidgetItem

"""GUI Draw imports"""
from GUI.MainWindow.DrawMainWindow import Ui_MainWindow
from GUI.BuscarPedido.DrawBuscarPedido import Ui_DIALOG_BuscaPedido
from GUI.EditarCNTR.DrawEditarCNTR import Ui_DIALOG_EditarCNTR
from GUI.EditarViagem.DrawEditarViagem import Ui_DIALOG_EditarViagem

from DataBase import *
from DateTools import *
from Objects import *

import sys

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.dataBase = DataBaseConnection()
        self.dateTools = DateTolls()
        self.setupUi(self)
        self.setupConnections()
        self.setupComboBox()
        self.NovoPedido()
        self.FillCNTRTable()

    def setupConnections(self):
        self.PBT_Salvar.clicked.connect(self.SalvarPedido)
        self.PBT_Novo.clicked.connect(self.NovoPedido)
        self.PBT_Buscar.clicked.connect(self.ShowBuscarPedido)
        self.PBT_IncluirCNTR.clicked.connect(self.ShowEditarCNTR)
        self.PBT_AplicarFiltro.clicked.connect(self.FillCNTRTable)
        self.PBT_EditarCNTR.clicked.connect(lambda: self.ShowEditarCNTR(False))
        self.PBT_Excluir.clicked.connect(self.ExcluirPedido)
        self.PBT_ExcluirCNTR.clicked.connect(self.ExcluirCNTR)
    
    def setupComboBox(self):
        self.CBX_Fabrica.clear()
        self.CBX_Porto.clear()
        self.CBX_Status.clear()
        self.CBX_StatusEstoque.clear()

        print(list(self.dataBase.GetFabricas()))
        self.CBX_Fabrica.addItems(self.dataBase.GetFabricas())
        self.CBX_Porto.addItems(list(self.dataBase.GetPortos()))
        self.CBX_Status.addItems(list(self.dataBase.GetStatusPedido()))
        self.CBX_StatusEstoque.addItems(list(self.dataBase.GetStatusCNTR()))

    #region NewCalls 
    def NovoPedido(self):
        self.TXB_Pedido.setText("")
        self.TXB_Booking.setText("")
        self.CBX_Status.currentIndex = 0
        self.CHB_Cabotagem.setChecked(False)
        self.CBX_Fabrica.currentIndex = 0
        self.CBX_Porto.currentIndex = 0
        self.DATE_DL_Fabrica.setDate(self.dateTools.today)
        self.DATE_DL_Porto.setDate(self.dateTools.today)
        self.DATE_InicioJanela.setDate(self.dateTools.today)
        self.DATE_FimJanela.setDate(self.dateTools.today)
        self.FillPedidoTable('')
    #endregion

    #region SaveCalls
    def SalvarPedido(self):
        novoPedido = Pedido(self.TXB_Pedido.text(),
                            self.TXB_Booking.text(),
                            self.CBX_Status.currentText(),
                            int(self.CHB_Cabotagem.isChecked()),
                            self.CBX_Fabrica.currentText(),
                            self.CBX_Porto.currentText(),
                            self.DATE_DL_Fabrica.text(),
                            self.DATE_DL_Porto.text(),
                            self.DATE_InicioJanela.text(),
                            self.DATE_FimJanela.text(),)
        
        self.dataBase.SavePedido(novoPedido)
    #endregion

    #region LoadCalls
    def CarregarPedido(self, _numeroPedido):
        datastream = self.dataBase.OpenPendido(str(_numeroPedido))
        self.TXB_Pedido.setText(str(datastream[0]))
        self.TXB_Booking.setText(str(datastream[2]))
        self.CBX_Status.setCurrentText(str(datastream[3]))
        self.CHB_Cabotagem.setChecked(bool(datastream[4]))
        self.CBX_Fabrica.setCurrentText(str(datastream[5]))
        self.CBX_Porto.setCurrentText(str(datastream[6]))
        self.DATE_DL_Fabrica.setDate(self.dateTools.GetDate(datastream[7]))
        self.DATE_DL_Porto.setDate(self.dateTools.GetDate(datastream[8]))
        self.DATE_InicioJanela.setDate(self.dateTools.GetDate(datastream[9]))
        self.DATE_FimJanela.setDate(self.dateTools.GetDate(datastream[10]))
        self.FillPedidoTable(str(datastream[2]))
    #endregion

    #region DeleteCalls
    def ExcluirPedido(self):
        self.dataBase.DeletePedido(self.TXB_Pedido.text())
        self.NovoPedido()
    
    def ExcluirCNTR(self):
        index = (self.TABLE_Estoque.selectionModel().currentIndex())
        value = index.sibling(index.row(), 0).data()
        self.dataBase.DeleteCNTR(value)
        self.FillCNTRTable()
    #endregion

    #region FillCalls
    def FillPedidoTable(self, booking):
        self.TABLE_Status.clear()
        
        dataStream = self.dataBase.FillPedidoTable(booking)

        names = ['Container', 'Status', 'Tara', 'Terminal', 'Armador', 'CPF', 'Motorista', 'Placa Cavalo', 'Placa Carreta', 'Expurgo']
        self.TABLE_Status.setRowCount(len(dataStream))
        self.TABLE_Status.setHorizontalHeaderLabels(names)

        for row in range(len(dataStream)):

            for col in range(len(dataStream[row])):

                self.TABLE_Status.setItem(row, col, QTableWidgetItem(str(dataStream[row][col])))
    
    def FillCNTRTable(self):

        self.TABLE_Estoque.clear()
        
        dataStream = self.dataBase.FillCNTRTable(self.TXB_BK.text(),
                                                 self.TXB_CNTR.text(),
                                                 self.CBX_StatusEstoque.currentText())

        names = ['Container', 'Booking', 'Status', 'Freetime', 'Armador', 'Terminal', 'Tara', 'Expurgo', 'CPF', 'Motorista', 'Placa Cavalo', 'Placa Carreta', 'OBS']
        
        self.TABLE_Estoque.setRowCount(len(dataStream))
        self.TABLE_Estoque.setHorizontalHeaderLabels(names)

        for row in range(len(dataStream)):

            for col in range(len(dataStream[row])):

                self.TABLE_Estoque.setItem(row, col, QTableWidgetItem(str(dataStream[row][col])))
    #endregion

    #region ShowCalls
    def ShowBuscarPedido(self):
        self.buscarPedidoDialog = BuscarPedidoDialog(self)
        self.buscarPedidoDialog.show()

    def ShowEditarCNTR(self, isNew = True):
        if (isNew):
            self.editarCNTRDIalog = EditarCNTRDialog(self)
        else:
            index = (self.TABLE_Estoque.selectionModel().currentIndex())
            value = index.sibling(index.row(), 0).data()
            self.editarCNTRDIalog = EditarCNTRDialog(self, value)
        
        self.editarCNTRDIalog.show()
    #endregion

class EditarCNTRDialog(QtWidgets.QDialog, Ui_DIALOG_EditarCNTR):
    def __init__(self, _parentWindow, cntr = None, parent = None):
        super(EditarCNTRDialog, self).__init__(parent)
        self.parentWindow = _parentWindow
        self.dataBase = DataBaseConnection()
        self.dateTools = DateTolls()
        self.setupUi(self)
        self.setupConnections()

        if not (cntr == None):
            self.OpenCNTR(cntr)

    def setupConnections(self):
        self.PBT_Gravar.clicked.connect(self.SalvarCNTR)
        self.PBT_Cancelar.clicked.connect(self.Fechar)

    def Fechar(self):
        self.hide()

    #region SaveCalls
    def SalvarCNTR(self):
        novoCNTR = CNTR(
                        self.TXB_Unidade.text(),
                        self.CBX_Status.currentText(),
                        self.TXB_Booking.text(),
                        self.SBX_Tara.text(),
                        self.CBX_Armador.currentText(),
                        self.CBX_TerminalVazio.currentText(),
                        self.DATE_Coleta.text(),
                        20,                                            #GAMBIARRA
                        '',
                        int(self.CHB_Expurgo.isChecked())
                        )
        
        self.dataBase.SaveCNTR(novoCNTR)
        self.parentWindow.FillCNTRTable()
        self.Fechar()
    #endregion

    #region LoadCalls
    def OpenCNTR(self, cntr):
        dataStream = self.dataBase.OpenCNTR(cntr)
        self.TXB_Unidade.setText(dataStream[0])
        self.CBX_Status.setCurrentText(dataStream[2])
        self.TXB_Booking.setText(dataStream[3])
        self.SBX_Tara.setValue(dataStream[4])
        self.CBX_Armador.setCurrentText(dataStream[5])
        self.CBX_TerminalVazio.setCurrentText(dataStream[6])
        self.DATE_Coleta.setDate(self.dateTools.GetDate(dataStream[7]))
        self.CHB_Expurgo.setChecked(bool(dataStream[10]))
    #endregion

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

    #region FillCalls
    def FillTable(self):
        self.TABLE_BuscarPedido.clear()

        dataStream = self.dataBase.FillPedidoSearch(self.CHB_TipoBusca.currentText().lower(),
                                                    self.TXB_Busca.text())

        names = ['Pedido', 'Booking', 'Status', 'Dead Line']
        self.TABLE_BuscarPedido.setHorizontalHeaderLabels(names)
        self.TABLE_BuscarPedido.setRowCount(len(dataStream))

        for row in range(len(dataStream)):

            for col in range(len(dataStream[row])):

                self.TABLE_BuscarPedido.setItem(row, col, QTableWidgetItem(str(dataStream[row][col])))
    #endregion

    #region SelectCalls
    def SelecionarPedido(self):
        index = (self.TABLE_BuscarPedido.selectionModel().currentIndex())
        value = index.sibling(index.row(), 0).data()
        
        self.parentWindow.CarregarPedido(value)
        self.hide()
    #endregion