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
        DIALOG_BuscaPedido.resize(326, 401)
        self.LBL_TipoBusca = QtWidgets.QLabel(DIALOG_BuscaPedido)
        self.LBL_TipoBusca.setGeometry(QtCore.QRect(10, 10, 121, 16))
        self.LBL_TipoBusca.setObjectName("LBL_TipoBusca")
        self.TABLE_BuscarPedido = QtWidgets.QTableWidget(DIALOG_BuscaPedido)
        self.TABLE_BuscarPedido.setGeometry(QtCore.QRect(10, 70, 401, 321))
        self.TABLE_BuscarPedido.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.TABLE_BuscarPedido.setObjectName("TABLE_BuscarPedido")
        self.TABLE_BuscarPedido.setColumnCount(3)
        self.TABLE_BuscarPedido.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.TABLE_BuscarPedido.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.TABLE_BuscarPedido.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.TABLE_BuscarPedido.setHorizontalHeaderItem(2, item)
        self.TXB_Busca = QtWidgets.QLineEdit(DIALOG_BuscaPedido)
        self.TXB_Busca.setGeometry(QtCore.QRect(10, 30, 113, 21))
        self.TXB_Busca.setObjectName("TXB_Busca")
        self.PBT_Selecionar = QtWidgets.QPushButton(DIALOG_BuscaPedido)
        self.PBT_Selecionar.setGeometry(QtCore.QRect(240, 20, 75, 31))
        self.PBT_Selecionar.setObjectName("PBT_Selecionar")
        self.TBN_Filtrar = QtWidgets.QToolButton(DIALOG_BuscaPedido)
        self.TBN_Filtrar.setGeometry(QtCore.QRect(130, 30, 25, 21))
        self.TBN_Filtrar.setObjectName("TBN_Filtrar")

        self.retranslateUi(DIALOG_BuscaPedido)
        QtCore.QMetaObject.connectSlotsByName(DIALOG_BuscaPedido)

    def retranslateUi(self, DIALOG_BuscaPedido):
        _translate = QtCore.QCoreApplication.translate
        DIALOG_BuscaPedido.setWindowTitle(_translate("DIALOG_BuscaPedido", "Buscar Pedido"))
        self.LBL_TipoBusca.setText(_translate("DIALOG_BuscaPedido", "Booking"))
        self.TABLE_BuscarPedido.setSortingEnabled(True)
        item = self.TABLE_BuscarPedido.horizontalHeaderItem(0)
        item.setText(_translate("DIALOG_BuscaPedido", "Pedido"))
        item = self.TABLE_BuscarPedido.horizontalHeaderItem(1)
        item.setText(_translate("DIALOG_BuscaPedido", "Booking"))
        item = self.TABLE_BuscarPedido.horizontalHeaderItem(2)
        item.setText(_translate("DIALOG_BuscaPedido", "Status"))
        self.PBT_Selecionar.setText(_translate("DIALOG_BuscaPedido", "Selecionar"))
        self.TBN_Filtrar.setText(_translate("DIALOG_BuscaPedido", "..."))
