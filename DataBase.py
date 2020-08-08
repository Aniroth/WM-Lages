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

        cntrsSTR = None
        for cntr in pedido.cntrs:
            cntrsSTR += cntr

        data = (pedido.numero, 0, pedido.booking, pedido.status, 
                pedido.cabotagem, pedido.expurgo, pedido.armador, 
                pedido.fabrica, pedido.porto, pedido.DLfabrica, pedido.DLporto,
                cntrsSTR, pedido.terminal, pedido.janelaInicio, pedido.janelaFim)
        
        self.cursor.execute("INSERT OR REPLACE INTO Pedidos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", data)
        self.conn.commit()
        self.CloseDB()