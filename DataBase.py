from typing import TypeVar
from Objects import *
import sqlite3

class DataBaseConnectionMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]

class DataBaseConnection(metaclass=DataBaseConnectionMeta):

    isDBopened = False

    def OpenDB(self):
        self.conn = sqlite3.connect('BancoDeDados\\Banco de Dados.db')
        self.cursor = self.conn.cursor()
        self.isDBopened = True
    
    def CloseDB(self):
        self.conn.close()

    def SavePedido(self, pedido):
        
        if not (self.isDBopened):
            self.OpenDB()

        dataStream = (
                      pedido.numero, 
                      1, 
                      pedido.booking, 
                      pedido.status, 
                      pedido.cabotagem, 
                      pedido.expurgo, 
                      pedido.armador, 
                      pedido.fabrica, 
                      pedido.porto, 
                      pedido.DLfabrica, 
                      pedido.DLporto,
                      pedido.janelaInicio, 
                      pedido.janelaFim, 
                      pedido.cntrs, 
                      pedido.terminal
                      )

        self.cursor.execute("INSERT OR REPLACE INTO Pedidos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", dataStream)
        self.conn.commit()
    
    def SaveCNTR(self, CNTR):

        if not (self.isDBopened):
            self.OpenDB()

        viagens = ''
        for i in CNTR.viagens:
            viagens += i + ' - '

        dataStream = (
                      CNTR.numero,
                      1,
                      CNTR.status,
                      CNTR.bookingFantasma,
                      CNTR.tara,
                      CNTR.bookingReal,
                      CNTR.pesoBruto,
                      viagens
                     )
        
        self.cursor.execute("INSERT OR REPLACE INTO CNTRs VALUES (?, ?, ?, ?, ?, ?, ?, ?)", dataStream)
        self.conn.commit()

        if not (CNTR.bookingReal == ''):
            self.InsertCNTRinPedido(CNTR)

    def OpenPendido(self, pedido):
        
        if not (self.isDBopened):
            self.OpenDB()

        self.cursor.execute("""
                            SELECT * FROM Pedidos
                            WHERE pedido = ?
                            """, (str(pedido),))
        
        dataStream = self.cursor.fetchone()

        return dataStream

    
    def GetCNTRs(self, booking):
        
        if not (self.isDBopened):
            self.OpenDB()
        
        self.cursor.execute("""
                            SELECT cntrs FROM Pedidos
                            WHERE booking = ?
                            """, (str(booking),))
        
        result = self.cursor.fetchone()

        if (result == None):
            return 'NULL_CNTR'
        else:
            return result[0]

    def InsertCNTRinPedido(self, CNTR):
        
        if not (self.isDBopened):
            self.OpenDB()

        self.cursor.execute("""
                            SELECT cntrs FROM Pedidos
                            WHERE booking = ?
                            """, (str(CNTR.bookingReal),))
        
        cntrResult = self.cursor.fetchone()
        cntr = cntrResult[0]

        if not (cntr == 'NULL_CNTR'):
            cntr += ' - '
        else:
            cntr = ''

        self.cursor.execute("""
                            UPDATE Pedidos 
                            SET cntrs = ? WHERE booking = ?
                            """, (str(cntr + CNTR.numero), str(CNTR.bookingReal),))
        self.conn.commit()

    def FillPedidoSearch(self, keySearch, valueSeach):
        
        if not (self.isDBopened):
            self.OpenDB()

        self.cursor.execute("""
                            SELECT pedido, booking, status, deadlinePorto FROM Pedidos
                            WHERE """ + str(keySearch) + " LIKE ?"
                            , ('%' + str(valueSeach) + '%',))
        
        result = self.cursor.fetchall()

        return result