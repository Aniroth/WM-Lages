from Objects import *
import sqlite3

#SINGLETON#
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
                      pedido.pedido, 
                      1, 
                      pedido.booking, 
                      pedido.status, 
                      pedido.cabotagem, 
                      pedido.fabrica, 
                      pedido.porto, 
                      pedido.DLfabrica, 
                      pedido.DLporto,
                      pedido.janelaInicio, 
                      pedido.janelaFim,
                      )

        self.cursor.execute("INSERT OR REPLACE INTO Pedidos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", dataStream)
        self.conn.commit()

    def SaveCNTR(self, CNTR):

        if not (self.isDBopened):
            self.OpenDB()

        dataStream = (
                      CNTR.cntr,
                      0,
                      CNTR.status,
                      CNTR.booking,
                      CNTR.tara,
                      CNTR.armador,
                      CNTR.terminal,
                      CNTR.dataColeta,
                      CNTR.freeTime,
                      CNTR.obs,
                      CNTR.expurgo
                     )
        
        self.cursor.execute("INSERT OR REPLACE INTO CNTRs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", dataStream)
        self.conn.commit()

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
    
    def OpenCNTR(self, cntr):
        
        if not (self.isDBopened):
            self.OpenDB()

        self.cursor.execute("""
                            SELECT * FROM CNTRs
                            WHERE cntr = ?
                            """, (str(cntr),))
        
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
    
    def GetViagens(self, cntr):

        if not (self.isDBopened):
            self.OpenDB()
        
        self.cursor.execute("""
                            SELECT ID FROM Viagens
                            WHERE cntr = ?
                            """, (str(cntr),))
        
        result = self.cursor.fetchone()

        if (result == None):
            return 'NULL_VIAGEM'
        else:
            return result[0]

    def InsertCNTRinPedido(self, CNTR):
        
        if not (self.isDBopened):
            self.OpenDB()

        try:
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
        except:
            return              #GAMBIARRA

    def FillPedidoSearch(self, keySearch, valueSeach):
        
        if not (self.isDBopened):
            self.OpenDB()

        self.cursor.execute("""
                            SELECT pedido, booking, status, deadlinePorto 
                            FROM Pedidos
                            WHERE """ + str(keySearch) + " LIKE ?"
                            , ('%' + str(valueSeach) + '%',))
        
        result = self.cursor.fetchall()

        return result
    
    def FillPedidoTable(self, booking):   #FALTA COMBINAR COM VIAGENS
        
        if not (self.isDBopened):
            self.OpenDB()

        self.cursor.execute("""
                            SELECT cntr, status, tara, terminal, armador
                            FROM CNTRs 
                            WHERE booking = ?
                            """
                            , (str(booking),))
        
        result = self.cursor.fetchall()

        return result
    
    def FillCNTRTable(self, booking, cntr, status):   #FALTA COMBINAR COM VIAGENS
        
        if not (self.isDBopened):
            self.OpenDB()

        if (booking == '' and cntr == '' and status ==''):    
            self.cursor.execute("""
                                SELECT cntr, booking, status, freetime, armador, terminal, tara, expurgo
                                FROM CNTRs 
                                """)

        else:
            self.cursor.execute("""
                                SELECT cntr, booking, status, freetime, armador, terminal, tara, expurgo
                                FROM CNTRs 
                                WHERE (booking = ? OR cntr = ? OR status = ?)
                                """
                                , (str(booking), str(cntr), str(status),))
        
        result = self.cursor.fetchall()

        return result