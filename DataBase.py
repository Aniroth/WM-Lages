from typing import TypeVar
from Objects import *
import sqlite3

class DataBaseConnection:

    def OpenDB(self):
        self.conn = sqlite3.connect('BancoDeDados\\Banco de Dados.db')
        self.cursor = self.conn.cursor()
    
    def CloseDB(self):
        self.conn.close()

    def SavePedido(self, pedido):
        self.OpenDB()

        dataStream = (pedido.numero, 1, pedido.booking, pedido.status, 
                pedido.cabotagem, pedido.expurgo, pedido.armador, 
                pedido.fabrica, pedido.porto, pedido.DLfabrica, pedido.DLporto,
                pedido.janelaInicio, pedido.janelaFim, pedido.cntrs, pedido.terminal)
        
        print (dataStream)

        self.cursor.execute("INSERT OR REPLACE INTO Pedidos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", dataStream)
        self.conn.commit()

        self.CloseDB()
    
    def FillPedidoSearch(self, keySearch, valueSeach):
        self.OpenDB()

        self.cursor.execute("""
                            SELECT pedido, booking, status, deadlinePorto FROM Pedidos
                            WHERE """ + str(keySearch) + " LIKE ?"
                            , ('%' + str(valueSeach) + '%',))
        

        result = self.cursor.fetchall()
        self.CloseDB()
        return result

