# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BuscarPedido.ui'
#
# Created by: PyQt5 UI code generator 5.15.0
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_DIALOG_BuscaPedido(object):
    def setupUi(self, DIALOG_BuscaPedido):
        DIALOG_BuscaPedido.setObjectName("DIALOG_BuscaPedido")
        DIALOG_BuscaPedido.resize(512, 401)
        self.LBL_TipoBusca = QtWidgets.QLabel(DIALOG_BuscaPedido)
        self.LBL_TipoBusca.setGeometry(QtCore.QRect(10, 10, 121, 16))
        self.LBL_TipoBusca.setObjectName("LBL_TipoBusca")
        self.CHB_TipoBusca = QtWidgets.QComboBox(DIALOG_BuscaPedido)
        self.CHB_TipoBusca.setGeometry(QtCore.QRect(10, 30, 131, 22))
        self.CHB_TipoBusca.setObjectName("CHB_TipoBusca")
        self.CHB_TipoBusca.addItem("")
        self.CHB_TipoBusca.addItem("")
        self.CHB_TipoBusca.addItem("")
        self.CHB_TipoBusca.addItem("")
        self.TABLE_BuscarPedido = QtWidgets.QTableWidget(DIALOG_BuscaPedido)
        self.TABLE_BuscarPedido.setGeometry(QtCore.QRect(10, 70, 491, 321))
        self.TABLE_BuscarPedido.setObjectName("TABLE_BuscarPedido")
        self.TABLE_BuscarPedido.setColumnCount(0)
        self.TABLE_BuscarPedido.setRowCount(0)
        self.TXB_Busca = QtWidgets.QLineEdit(DIALOG_BuscaPedido)
        self.TXB_Busca.setGeometry(QtCore.QRect(150, 30, 113, 21))
        self.TXB_Busca.setObjectName("TXB_Busca")
        self.PBT_Selecionar = QtWidgets.QPushButton(DIALOG_BuscaPedido)
        self.PBT_Selecionar.setGeometry(QtCore.QRect(430, 20, 75, 31))
        self.PBT_Selecionar.setObjectName("PBT_Selecionar")

        self.retranslateUi(DIALOG_BuscaPedido)
        QtCore.QMetaObject.connectSlotsByName(DIALOG_BuscaPedido)

    def retranslateUi(self, DIALOG_BuscaPedido):
        _translate = QtCore.QCoreApplication.translate
        DIALOG_BuscaPedido.setWindowTitle(_translate("DIALOG_BuscaPedido", "Buscar Pedido"))
        self.LBL_TipoBusca.setText(_translate("DIALOG_BuscaPedido", "Buscar por"))
        self.CHB_TipoBusca.setItemText(0, _translate("DIALOG_BuscaPedido", "pedido"))
        self.CHB_TipoBusca.setItemText(1, _translate("DIALOG_BuscaPedido", "booking"))
        self.CHB_TipoBusca.setItemText(2, _translate("DIALOG_BuscaPedido", "status"))
        self.CHB_TipoBusca.setItemText(3, _translate("DIALOG_BuscaPedido", "deadlinePorto"))
        self.PBT_Selecionar.setText(_translate("DIALOG_BuscaPedido", "Selecionar"))