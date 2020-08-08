import sys

from LogicMainWindow import Logic_MainWindow
from Pedidos import Pedido

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    form = Logic_MainWindow()
    form.showMaximized()
    app.exec_()

if __name__ == '__main__':
    main()