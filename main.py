from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
from GUI.MainWindow.LogicMainWindow import Logic_MainWindow
import sys
from Pedidos import Pedido
from DataBaseHandler import SavePedido

def main():
    a = Pedido(53251, 'Teste', 'aaaaaa', 'aaaaa', 'dasdasdasd','dsadasda','20-05-20','21-05-20')
    SavePedido(a)
    """
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    form = Logic_MainWindow()
    form.showMaximized()
    app.exec_()"""

if __name__ == '__main__':
    main()