"""PyQT imports"""
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QMessageBox, QCompleter

"""GUI Draw imports"""
from GUI.MainWindow.DrawMainWindow import Ui_MainWindow
from GUI.BuscarPedido.DrawBuscarPedido import Ui_DIALOG_BuscaPedido
from GUI.EditarCNTR.DrawEditarCNTR import Ui_DIALOG_EditarCNTR
from GUI.EditarViagem.DrawEditarViagem import Ui_DIALOG_EditarViagem
from GUI.EditarBooking.DrawEditarBooking import Ui_DIALOG_NovoBooking

from DataBase import *
from Tools import *
from Objects import *

import sys
import os
import pathlib

class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.dataBase = DataBaseConnection()
        self.tools = Tools()
        self.setupUi(self)
        self.setupConnections()
        self.setupComboBox()
        self.DATE_DataViagem.setDate(self.tools.today)
        scriptDir = str(pathlib.Path().absolute())
        self.setWindowIcon(QtGui.QIcon(scriptDir + '\\icon.png'))
        self.FillCNTRTable()
        self.FillViagensTable()
        self.showMaximized()
        if (self.OpenBooking('') == True):
            self.ShowNovoBooking()


    def setupConnections(self):
        self.PBT_Salvar.clicked.connect(self.SaveBooking)
        self.PBT_Novo.clicked.connect(self.ShowNovoBooking)
        self.PBT_Buscar.clicked.connect(self.ShowBuscarBooking)
        self.PBT_Excluir.clicked.connect(self.DeleteBooking)
        self.PBT_ExcluirCNTR.clicked.connect(self.DeleteCNTR)
        self.PBT_AplicarFiltro.clicked.connect(self.FillCNTRTable)
        self.PBT_EditarCNTR.clicked.connect(lambda: self.ShowEditarCNTR(False))
        self.PBT_IncluirCNTR.clicked.connect(lambda: self.ShowEditarCNTR(True))
        self.PBT_NovaViagem.clicked.connect(lambda: self.ShowEditarViagem(True))
        self.PBT_FiltroViagem.clicked.connect(self.FillViagensTable)
        self.PBT_EditarViagem.clicked.connect(lambda: self.ShowEditarViagem(False))
        self.PBT_ExcluirViagem.clicked.connect(self.DeleteViagem)
        self.TABLE_Status.cellClicked.connect(self.AllowEdit)
    
    def setupComboBox(self):
        self.CBX_Fabrica.clear()
        self.CBX_Porto.clear()
        self.CBX_Status.clear()
        self.CBX_StatusEstoque.clear()
        self.CBX_StatusViagem.clear()
        self.CBX_Fabrica.addItems(self.dataBase.GetFabricas())
        self.CBX_Porto.addItems(list(self.dataBase.GetPortos()))
        self.CBX_Status.addItems(list(self.dataBase.GetStatusPedido()))
        self.CBX_StatusEstoque.addItems(list(self.dataBase.GetStatusCNTR()))
        self.CBX_StatusViagem.addItems(list(self.dataBase.GetTipoViagem()))
        self.CBX_Status.setCurrentText('')
        self.CBX_StatusEstoque.setCurrentText('')
        self.CBX_StatusViagem.addItem('')
        self.CBX_StatusViagem.setCurrentText('')

    #region SaveCalls
    def SaveBooking(self):
        booking = Booking(self.TXB_Booking.text(),
                          self.CBX_Status.currentText(),
                          self.CHB_Cabotagem.isChecked(),
                          self.CBX_Fabrica.currentText(),
                          self.CBX_Porto.currentText(),
                          self.DATE_Apartir.text(),
                          self.DATE_DL_Porto.text(),
                          self.SBX_QtdePedido.text())

        ofertas = []

        for i in range(self.TABLE_Status.rowCount()):
            ID = self.TABLE_Status.item(i, 0).text()
            oferta = self.TABLE_Status.item(i, 1).text()
            ofertas.append(Oferta(self.TXB_Booking.text(),
                                  oferta,
                                  ID       
                                  ))

        self.dataBase.SaveBooking(booking)
        self.dataBase.SaveOfertas(ofertas)
    #endregion

    #region LoadCalls
    def OpenBooking(self, booking):
        if not (booking == ''):
            self.UpdateBooking(booking)
        
        datastream = self.dataBase.OpenBooking(str(booking))

        if (datastream == None):
            
            ret = QMessageBox.warning(self, 
                                        'Nenhum booking no banco de dados!',
                                        'Você deve clicar em "Novo Booking" para cadastrar.',
                                        QMessageBox.Ok, QMessageBox.Ok)

            if (ret == QMessageBox.Ok):
                return 

        self.TXB_Booking.setText(datastream[1])
        self.CBX_Status.setCurrentText(datastream[2])
        self.CHB_Cabotagem.setChecked(bool(datastream[3]))
        self.CBX_Fabrica.setCurrentText(datastream[4])
        self.CBX_Porto.setCurrentText(datastream[5])
        self.DATE_Apartir.setDate(self.tools.GetDate(datastream[6]))
        self.DATE_DL_Porto.setDate(self.tools.GetDate(datastream[7]))
        self.SBX_QtdePedido.setValue(int(datastream[8]))
        self.FillBookingTable(str(datastream[1]))
    #endregion

    #region DeleteCalls
    def DeleteBooking(self):
        self.dataBase.DeleteBooking(self.TXB_Booking.text())
        self.OpenBooking('')
    
    def DeleteCNTR(self):
        index = self.TABLE_Estoque.selectionModel().currentIndex()
        value = index.sibling(index.row(), 0).data()
        self.dataBase.DeleteCNTR(value)
        self.FillCNTRTable()
    
    def DeleteViagem(self):
        index = self.TABLE_Viagens.selectionModel().currentIndex()
        value = index.sibling(index.row(), 0).data()
        self.dataBase.DeleteViagem(value)
        self.FillViagensTable()
    #endregion

    #region FillCalls
    def FillBookingTable(self, booking):
        self.TABLE_Status.clear()
        
        dataStream = self.dataBase.FillBookingTable(booking)

        names = ['ID', 'Oferta', 'Container', 'Status', 'Tara', 'Lacre', 'Terminal', 'Armador', 'Expurgo', 'OBS']
        self.TABLE_Status.setRowCount(len(dataStream))
        self.TABLE_Status.setColumnCount(len(names))
        self.TABLE_Status.setHorizontalHeaderLabels(names)

        for row in range(len(dataStream)):

            for col in range(len(dataStream[row])):
                
                itemText = self.tools.FormatData(dataStream[row][col])
                self.TABLE_Status.setItem(row, col, QTableWidgetItem(itemText))
    
    def FillCNTRTable(self):

        self.TABLE_Estoque.clear()
        
        dataStream = self.dataBase.FillCNTRTable(self.TXB_BK.text(),
                                                 self.TXB_CNTR.text(),
                                                 self.CBX_StatusEstoque.currentText())

        names = ['Container', 'Booking', 'Status', 'Freetime', 'Armador', 'Terminal', 'Tara', 'Lacre', 'Agendamento', 'Data Agendamento', 'Expurgo', 'OBS']
        
        self.TABLE_Estoque.setRowCount(len(dataStream))
        self.TABLE_Estoque.setColumnCount(len(names))
        self.TABLE_Estoque.setHorizontalHeaderLabels(names)

        for row in range(len(dataStream)):

            for col in range(len(dataStream[row])):
                
                itemText = self.tools.FormatData(dataStream[row][col])
                self.TABLE_Estoque.setItem(row, col, QTableWidgetItem(itemText))
    
    def FillViagensTable(self):

        self.TABLE_Viagens.clear()
        
        dataStream = self.dataBase.FillViagensTable(self.TXB_CNTRViagem.text(),
                                                    self.TXB_BookingViagem.text(),
                                                    self.CBX_StatusViagem.currentText(),
                                                    self.DATE_DataViagem.text(),
                                                    bool(self.CHB_SelectALL.isChecked()))

        names = ['ID', 'Status', 'Tipo', 'Booking', 'CNTR', 'Início', 'Fim', 'Origem', 'Destino', 'Lacre', 'CPF', 'Motorista', 'Placa Cavalo', 'Placa Carreta', 'Placa Carreta 2', 'Spot']
        
        self.TABLE_Viagens.setRowCount(len(dataStream))
        self.TABLE_Viagens.setColumnCount(len(names))
        self.TABLE_Viagens.setHorizontalHeaderLabels(names)

        for row in range(len(dataStream)):

            for col in range(len(dataStream[row])):
                
                itemText = self.tools.FormatData(dataStream[row][col])
                self.TABLE_Viagens.setItem(row, col, QTableWidgetItem(itemText))
    #endregion

    #region ShowCalls
    def ShowNovoBooking(self):
        self.editarBookingDialog = EditarBookingDialog(self)
        self.editarBookingDialog.show()
    
    def ShowBuscarBooking(self):
        self.buscarBookingDialog = BuscarBookingDialog(self)
        self.buscarBookingDialog.show()

    def ShowEditarCNTR(self, isNew):
        if (isNew):
            self.editarCNTRDialog = EditarCNTRDialog(self)
        else:
            index = (self.TABLE_Estoque.selectionModel().currentIndex())
            value = index.sibling(index.row(), 0).data()
            self.editarCNTRDialog = EditarCNTRDialog(self, value)
        
        self.editarCNTRDialog.show()
    
    def ShowEditarViagem(self, isNew):
        if (isNew):
            self.editarViagemDialog = EditarViagemDialog(self)
        else:
            index = (self.TABLE_Viagens.selectionModel().currentIndex())
            value = index.sibling(index.row(), 0).data()
            self.editarViagemDialog = EditarViagemDialog(self, value)
        
        self.editarViagemDialog.show()
    #endregion

    def AllowEdit(self):

        index = (self.TABLE_Status.selectionModel().currentIndex())

        if (index.column() == 1):
            self.TABLE_Status.setEditTriggers(QtWidgets.QAbstractItemView.DoubleClicked)
        else:
            self.TABLE_Status.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
    
    def UpdateBooking(self, booking):
        
        isAberto = False
        isUnitizando = False
        isEnvioPorto = False
        finalizadoCount = 0
        cntrs = self.dataBase.GetCNTRs(booking)

        for status in cntrs:

            if (status == '' or 'Vázio'):
                isAberto = True
            elif (status == 'Trânsito Fábrica' or status == 'Unitizado'):
                isUnitizando = True
            elif (status == 'Trânsito Porto'):
                isEnvioPorto = True
            elif (status == 'Finalizado'):
                finalizadoCount += 1

        if (finalizadoCount == len(self.dataBase.getofe)):
            self.dataBase.UpdateBookingStatus(booking, 'Finalizado')
        elif (isEnvioPorto):
            self.dataBase.UpdateBookingStatus(booking, 'Envio Porto')
        elif (isUnitizando):
            self.dataBase.UpdateBookingStatus(booking, 'Unitização')
        elif (isAberto):
            self.dataBase.UpdateBookingStatus(booking, 'Aberto')

class BuscarBookingDialog(QtWidgets.QDialog, Ui_DIALOG_BuscaPedido):
    def __init__(self, _parentWindow, parent = None):
        super(BuscarBookingDialog, self).__init__(parent)
        self.parentWindow = _parentWindow
        self.setupUi(self)
        self.setupConnections()
        self.dataBase = DataBaseConnection()
        self.FillTable()
        scriptDir = str(pathlib.Path().absolute())
        self.setWindowIcon(QtGui.QIcon(scriptDir + '\\icon.png'))
    
    def setupConnections(self):
        self.TBN_Filtrar.clicked.connect(self.FillTable)
        self.PBT_Selecionar.clicked.connect(self.SelecionarPedido)

    #region FillCalls
    def FillTable(self):
        self.TABLE_BuscarPedido.clear()

        dataStream = self.dataBase.FillBookingSearch(self.TXB_Busca.text())

        names = ['Booking', 'Status', 'Dead Line']
        self.TABLE_BuscarPedido.setRowCount(len(dataStream))
        self.TABLE_BuscarPedido.setColumnCount(len(names))
        self.TABLE_BuscarPedido.setHorizontalHeaderLabels(names)

        for row in range(len(dataStream)):

            for col in range(len(dataStream[row])):

                self.TABLE_BuscarPedido.setItem(row, col, QTableWidgetItem(str(dataStream[row][col])))
    #endregion

    #region SelectCalls
    def SelecionarPedido(self):
        index = (self.TABLE_BuscarPedido.selectionModel().currentIndex())
        value = index.sibling(index.row(), 0).data()
        
        self.parentWindow.OpenBooking(value)
        self.hide()
    #endregion

class EditarBookingDialog(QtWidgets.QDialog, Ui_DIALOG_NovoBooking):
    def __init__(self, _parentWindow, parent=None):
        super(EditarBookingDialog, self).__init__(parent)
        self.dataBase = DataBaseConnection()
        self.dateTools = Tools()
        self.parentWindow = _parentWindow
        self.setupUi(self)
        self.setupConnections()
        self.setupComboBox()
        scriptDir = str(pathlib.Path().absolute())
        self.setWindowIcon(QtGui.QIcon(scriptDir + '\\icon.png'))

    def setupConnections(self):        
        self.PBT_Gravar.clicked.connect(self.SaveBooking)
    
    def setupComboBox(self):
        self.DATE_Apartir.setDate(self.dateTools.today)
        self.DATE_DL_Porto.setDate(self.dateTools.today)
        self.CBX_Fabrica.addItems(self.dataBase.GetFabricas())
        self.CBX_Porto.addItems(self.dataBase.GetPortos())
    
    def SaveBooking(self):
        novoBooking = Booking(self.TXB_Booking.text(),
                              'Aberto',
                              self.CHB_Cabotagem.isChecked(),
                              self.CBX_Fabrica.currentText(),
                              self.CBX_Porto.currentText(),
                              self.DATE_Apartir.text(),
                              self.DATE_DL_Porto.text(),
                              self.SBX_QtdePedido.text())
        
        self.dataBase.SaveBooking(novoBooking)
        self.CreateOfertas(int(self.SBX_QtdePedido.text()), 
                           self.TXB_Booking.text())
        self.parentWindow.OpenBooking(novoBooking.booking)
        self.parentWindow.FillViagensTable()
        self.parentWindow.FillCNTRTable()
        self.hide()
    
    def CreateOfertas(self, qtde, booking):
        novaOferta = Oferta(booking)
        self.dataBase.NewOferta(novaOferta, qtde)

class EditarCNTRDialog(QtWidgets.QDialog, Ui_DIALOG_EditarCNTR):
    def __init__(self, _parentWindow, _cntr = None, parent = None):
        super(EditarCNTRDialog, self).__init__(parent)
        self.parentWindow = _parentWindow
        self.dataBase = DataBaseConnection()
        self.tools = Tools()
        self.setupUi(self)
        self.setupConnections()
        self.setupComboBox()
        scriptDir = str(pathlib.Path().absolute())
        self.setWindowIcon(QtGui.QIcon(scriptDir + '\\icon.png'))

        if (_cntr == None):
            self.DATE_Coleta.setDate(self.tools.today)
            self.DATE_Agendamento.setDate(self.tools.today)
            self.CBX_Agendamento.hide()
            self.LBL_Agendamento.hide()
            self.DATE_Agendamento.hide()
            self.LBL_AgendamentoPorto.hide()
            self.cntr = None
        else:
            self.OpenCNTR(_cntr)
            self.cntr = _cntr

    def setupConnections(self):
        self.PBT_Gravar.clicked.connect(self.SalvarCNTR)
        self.PBT_Cancelar.clicked.connect(self.Fechar)

    def setupComboBox(self):
        self.CBX_Armador.clear()
        self.CBX_Status.clear()
        self.CBX_TerminalVazio.clear()
        self.CBX_Armador.addItems(self.dataBase.GetArmadores())
        self.CBX_Status.addItems(self.dataBase.GetStatusCNTR())
        self.CBX_TerminalVazio.addItems(self.dataBase.GetTerminais())

    def Fechar(self):
        self.hide()

    #region SaveCalls
    def SalvarCNTR(self):

        agendamento = self.CBX_Agendamento.currentText()
        dataAgendamento = self.DATE_Agendamento.text()

        if not (self.ValidateCNTR()):
            return

        if (self.cntr == None):

            self.novaViagem = EditarViagemDialog(self.parentWindow)
            self.novaViagem.TXB_CNTR.setText(self.TXB_Unidade.text())
            self.novaViagem.CBX_Origem.setCurrentText(self.CBX_TerminalVazio.currentText())
            self.novaViagem.CBX_Destino.setCurrentText('Lages')
            self.novaViagem.CBX_StatusViagem.setCurrentText('Finalizada')
            self.novaViagem.CBX_TipoViagem.setCurrentText('Coleta Vázio')
            self.novaViagem.DATE_Inicio.setDate(self.tools.today)
            self.novaViagem.DATE_Fim.setDate(self.tools.today)
            agendamento = ''
            dataAgendamento = ''
            self.novaViagem.show()

        elif (self.CBX_Status.currentText() == 'Trânsito Fábrica'):

            if (self.dataBase.GetViagemByCNTR(self.TXB_Unidade.text(), 'Unitização Fábrica') == None):
                self.novaViagem = EditarViagemDialog(self.parentWindow)
                self.novaViagem.TXB_CNTR.setText(self.TXB_Unidade.text())
                self.novaViagem.CBX_Origem.setCurrentText('Lages')
                self.novaViagem.CBX_Destino.setCurrentText(self.dataBase.GetFabrica(self.TXB_Booking.text()))
                self.novaViagem.CBX_StatusViagem.setCurrentText('Em Trânsito')
                self.novaViagem.CBX_TipoViagem.setCurrentText('Unitização Fábrica')
                self.novaViagem.DATE_Inicio.setDate(self.tools.today)
                self.novaViagem.DATE_Fim.setDate(self.tools.today)
                self.novaViagem.show()

        elif (self.CBX_Status.currentText() == 'Unitizado'):

            self.dataBase.CloseViagem(self.TXB_Unidade.text(),
                                      'Unitização Fábrica')

        elif (self.CBX_Status.currentText() == 'Trânsito Porto'):

            if (self.dataBase.GetViagemByCNTR(self.TXB_Unidade.text(), 'Envio Porto') == None):
                self.novaViagem = EditarViagemDialog(self.parentWindow)
                self.novaViagem.TXB_CNTR.setText(self.TXB_Unidade.text())
                self.novaViagem.CBX_Origem.setCurrentText('Lages')
                self.novaViagem.CBX_Destino.setCurrentText(self.dataBase.GetPorto(self.TXB_Booking.text()))
                self.novaViagem.CBX_StatusViagem.setCurrentText('Em Trânsito')
                self.novaViagem.CBX_TipoViagem.setCurrentText('Envio Porto')
                self.novaViagem.DATE_Inicio.setDate(self.tools.today)
                self.novaViagem.DATE_Fim.setDate(self.tools.today)
                self.novaViagem.show()

        elif (self.CBX_Status.currentText() == 'Finalizado'):
            self.dataBase.CloseViagem(self.TXB_Unidade.text(),
                                      'Envio Porto')

        novoCNTR = CNTR(
                self.TXB_Unidade.text(),
                self.CBX_Status.currentText(),
                self.TXB_Booking.text(),
                self.SBX_Tara.text(),
                self.CBX_Armador.currentText(),
                self.CBX_TerminalVazio.currentText(),
                self.DATE_Coleta.text(),
                20,                                            #GAMBIARRA
                self.TED_obs.toPlainText(),
                int(self.CHB_Expurgo.isChecked()),
                self.TXB_Oferta.text(),
                self.TXB_Lacre.text(),
                agendamento,
                dataAgendamento
                )

        self.dataBase.SaveCNTR(novoCNTR)
        self.parentWindow.FillViagensTable()
        self.parentWindow.FillCNTRTable()
        self.parentWindow.OpenBooking(self.TXB_Booking.text())
        self.Fechar()
    #endregion

    #region LoadCalls
    def OpenCNTR(self, cntr):
        dataStream = self.dataBase.OpenCNTR(cntr)
        self.TXB_Unidade.setText(dataStream[1])
        self.TXB_Oferta.setText(str(dataStream[2]))
        self.CBX_Status.setCurrentText(dataStream[3])
        self.TXB_Booking.setText(dataStream[4])
        self.SBX_Tara.setValue(dataStream[5])
        self.CBX_Armador.setCurrentText(dataStream[6])
        self.CBX_TerminalVazio.setCurrentText(dataStream[7])
        self.DATE_Coleta.setDate(self.tools.GetDate(dataStream[8]))
        self.TED_obs.setText(dataStream[10])
        self.CHB_Expurgo.setChecked(bool(dataStream[11]))
        self.TXB_Lacre.setText(dataStream[12])
        self.CBX_Agendamento.addItem('')
        self.CBX_Agendamento.addItems(self.dataBase.Agendamentos(self.dataBase.GetPorto(self.TXB_Booking.text())))
        self.CBX_Agendamento.setCurrentText(dataStream[13])
        
        if (dataStream[14] == ''):
            self.DATE_Agendamento.setDate(self.tools.GetDate(self.dataBase.GetDeadLine(dataStream[4])))
        else:
            self.DATE_Agendamento.setDate(self.tools.GetDate(dataStream[14]))
    #endregion

    def ValidateCNTR(self):

        if (self.dataBase.GetBooking(self.TXB_Booking.text()) == None):
            
            ret = QMessageBox.warning(self, 
                                        'Booking não encontrado!',
                                        'O booking digitado não foi encontrado\nVerifique se a numeração está correta\n\nSe você acredita que isso é um erro, abra um chamado!',
                                        QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)

            if (ret == QMessageBox.Cancel):
                return False
        
        if (self.dataBase.GetOferta(self.TXB_Oferta.text()) == None and not self.TXB_Oferta.text() == ''):
            
            ret = QMessageBox.critical(self, 
                                        'Oferta não encontrada!',
                                        'Não foi possível localizar a oferta digitada, você não pode prosseguir\nSe você acredita que isso é um erro, abra um chamado!',
                                        QMessageBox.Ok, QMessageBox.Ok)

            if (ret == QMessageBox.Ok):
                return False

        if (self.CBX_Status.currentText() == 'Trânsito Porto'):

            if (self.CBX_Agendamento.currentText() == ''):
                ret = QMessageBox.warning(self, 
                                            'Agendamento em branco!',
                                            'O agendamento não foi preenchido\nSe você acredita que isso é um erro, abra um chamado!',
                                            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)

                if (ret == QMessageBox.Cancel):
                    return False

            if (self.TXB_Lacre.text() == ''):
                ret = QMessageBox.warning(self, 
                                            'Lacre em branco!',
                                            'O lacre não foi preenchido\nSe você acredita que isso é um erro, abra um chamado!',
                                            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
                
                if (ret == QMessageBox.Cancel):
                    return False
            
            if (self.dataBase.GetViagemByCNTR(self.TXB_Unidade.text(), 'Unitização Fábrica') == None):
                
                ret = QMessageBox.warning(self, 
                                            'Viagem para fábrica não encontrada',
                                            """Não foi possível encontrar uma viagem de unitização para esse CNTR
                                                \nVocê pode prosseguir mesmo assim, mas para garantir os relatórios corretos
                                                \né indicado que todas as viagens estejam de acordo
                                                \nSe você acredita que isso é um erro, abra um chamado!""",
                                            QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)
                
                if (ret == QMessageBox.Cancel):
                    return False
        
        return True

class EditarViagemDialog(QtWidgets.QDialog, Ui_DIALOG_EditarViagem):
    def __init__(self, _parentWindow, _viagem = None, parent=None):
        super(EditarViagemDialog, self).__init__(parent)
        self.dataBase = DataBaseConnection()
        self.dateTools = Tools()
        self.parentWindow = _parentWindow
        self.setupUi(self)
        self.setupConnections()
        self.setupComboBox()
        self.viagem = _viagem
        scriptDir = str(pathlib.Path().absolute())
        self.setWindowIcon(QtGui.QIcon(scriptDir + '\\icon.png'))

        if not (_viagem == None):
            self.OpenViagem()

        if (self.viagem == None):
            self.DATE_Fim.setDate(self.dateTools.today)
            self.DATE_Inicio.setDate(self.dateTools.today)

    def setupConnections(self):
        self.TXB_CPF.editingFinished.connect(self.AutoFillConjunto)
        self.PBT_Gravar.clicked.connect(self.SaveViagem)
        self.PBT_Cancelar.clicked.connect(self.Fechar)
    
    def setupComboBox(self):
        self.CBX_Carreta.clear()
        self.CBX_Cavalo.clear()
        self.CBX_Destino.clear()
        self.CBX_Motorista.clear()
        self.CBX_Origem.clear()
        self.CBX_StatusViagem.clear()
        self.CBX_TipoViagem.clear()
        self.CBX_Motorista.addItems(self.dataBase.GetMotorista())
        self.CBX_Cavalo.addItems(self.dataBase.GetCavalo())
        self.CBX_Carreta.addItems(self.dataBase.GetCarreta())
        self.CBX_Carreta_2.addItems(self.dataBase.GetCarreta2())
        self.CBX_Origem.addItems(self.dataBase.GetTerminais())
        self.CBX_Origem.addItems(self.dataBase.GetFabricas())
        self.CBX_Destino.addItems(self.dataBase.GetFabricas())
        self.CBX_Destino.addItems(self.dataBase.GetPortos())
        self.CBX_StatusViagem.addItems(self.dataBase.GetStatusViagem())
        self.CBX_TipoViagem.addItems(self.dataBase.GetTipoViagem())
        model = QtCore.QStringListModel(self.dataBase.GetCPFs())
        completer = QCompleter()
        completer.setModel(model)
        self.TXB_CPF.setCompleter(completer)
    
    def Fechar(self):
        self.hide()

    def AutoFillConjunto(self):
        cpf = self.TXB_CPF.text()

        if (self.dataBase.GetMotorista(cpf) == None):
            
            ret = QMessageBox.warning(self, 
                                        'CPF Inválido',
                                        'O CPF digitado não foi enconrado\n\nPara cadastrar motoristas, edite o arquivo excel Banco Manual',
                                        QMessageBox.Ok, QMessageBox.Ok)

            if (ret == QMessageBox.Ok):
                return
            else:
                return

        self.CBX_Motorista.setCurrentText(self.dataBase.GetMotorista(cpf))
        self.CBX_Cavalo.setCurrentText(self.dataBase.GetCavalo(cpf))
        self.CBX_Carreta.setCurrentText(self.dataBase.GetCarreta(cpf))
        self.CBX_Carreta_2.setCurrentText(self.dataBase.GetCarreta2(cpf))

    def SaveViagem(self):
        NovaViagem = Viagem(self.CBX_StatusViagem.currentText(),
                            self.TXB_CNTR.text(),
                            self.CBX_TipoViagem.currentText(),
                            self.DATE_Inicio.text(),
                            self.DATE_Fim.text(),
                            self.CBX_Origem.currentText(),
                            self.CBX_Destino.currentText(),
                            self.TXB_CPF.text(),
                            self.CBX_Motorista.currentText(),
                            self.CBX_Cavalo.currentText(),
                            self.CBX_Carreta.currentText(),
                            int(self.CHB_Spot.isChecked()),
                            self.CBX_Carreta_2.currentText(),
                            self.viagem)
        
        if (self.dataBase.GetMotorista(cpf) == None):
            
            ret = QMessageBox.warning(self, 
                                        'Motorista não cadastrado',
                                        'O motorista atual não está cadastrado\n\nVocê pode prosseguir mesmo assim, mas é recomendado o cadastro no arquivo Excel Banco Manual',
                                        QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Cancel)

            if (ret == QMessageBox.Cancel):
                return

        self.dataBase.SaveViagem(NovaViagem)
        self.parentWindow.FillViagensTable()
        self.parentWindow.FillCNTRTable()
        self.Fechar()

    def OpenViagem(self):
        dataStream = self.dataBase.OpenViagem(self.viagem)
        self.CBX_StatusViagem.setCurrentText(dataStream[2])
        self.TXB_CNTR.setText(dataStream[3])
        self.CBX_TipoViagem.setCurrentText(dataStream[4])
        self.DATE_Inicio.setDate(self.dateTools.GetDate(dataStream[5]))
        self.DATE_Fim.setDate(self.dateTools.GetDate(dataStream[6]))
        self.CBX_Origem.setCurrentText(dataStream[7])
        self.CBX_Destino.setCurrentText(dataStream[8])
        self.TXB_CPF.setText(dataStream[9])
        self.CBX_Motorista.setCurrentText(dataStream[10])
        self.CBX_Cavalo.setCurrentText(dataStream[11])
        self.CBX_Carreta.setCurrentText(dataStream[12])
        self.CBX_Carreta_2.setCurrentText(dataStream[13])
        self.CHB_Spot.setChecked(dataStream[14])