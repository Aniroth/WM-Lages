from PyQt5.QtWidgets import QApplication
from LogicGUI import MainWindow
from DataBase import DataBaseConnection

import sys

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    form = MainWindow()
    form.showMaximized()
    app.exec_()
    dataBase = DataBaseConnection()
    app.lastWindowClosed.connect(dataBase.CloseDB(dataBase))

if __name__ == '__main__':
    main()