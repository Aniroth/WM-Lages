from PyQt5.QtWidgets import QApplication
from LogicGUI import MainWindow

import sys

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    form = MainWindow()
    form.showMaximized()
    app.exec_()

if __name__ == '__main__':
    main()