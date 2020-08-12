from PyQt5.QtWidgets import QApplication, QStyleFactory
from LogicGUI import MainWindow
from DataBase import DataBaseConnection

import sys

def main():
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('fusion'))
    form = MainWindow()
    form.showMaximized()
    app.exec_()

if __name__ == '__main__':
    main()