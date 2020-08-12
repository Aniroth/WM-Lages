from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5 import QtGui
from LogicGUI import MainWindow
from DataBase import DataBaseConnection

import sys
import os

def main():
    ver = '1.0'
    dataBase = DataBaseConnection()

    if not (ver == dataBase.GetVersion()):
        print('VERSÃO DESATUALIZADA!!!')
        resp = input('\n\nPressione Y para atualizar ou N para fechar\n\n').lower()
        return

    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('fusion'))
    scriptDir = os.path.dirname(os.path.realpath(__file__))
    app.setWindowIcon(QtGui.QIcon(scriptDir + os.path.sep + 'icon.png'))
    form = MainWindow()
    form.showMaximized()
    app.exec_()

if __name__ == '__main__':
    main()