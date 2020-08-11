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

    #region SaveQueries
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
        
    def SaveViagem(self, Viagem):
                
        if not (self.isDBopened):
            self.OpenDB()

        dataStream = (
                      Viagem.ID,
                      0,
                      Viagem.status,
                      Viagem.cntr,
                      Viagem.tipoViagem,
                      Viagem.inicio,
                      Viagem.fim,
                      Viagem.origem,
                      Viagem.destino,
                      Viagem.CPF,
                      Viagem.motorista,
                      Viagem.cavalo,
                      Viagem.carreta,
                      Viagem.spot
                      )

        self.cursor.execute("INSERT OR REPLACE INTO Pedidos VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, )", dataStream)
        self.conn.commit()
    #endregion

    #region LoadQueries
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
    #endregion

    #region DeleteQueries
    def DeletePedido(self, pedido):
        
        if not (self.isDBopened):
            self.OpenDB()
        
        self.cursor.execute("""
                            DELETE FROM Pedidos
                            WHERE pedido = ?
                            """, (str(pedido),))
        
        self.conn.commit()
    
    def DeleteCNTR(self, cntr):
        
        if not (self.isDBopened):
            self.OpenDB()
        
        self.cursor.execute("""
                            DELETE FROM CNTRs
                            WHERE cntr= ?
                            """, (str(cntr),))
        
        self.conn.commit()

    #endregion

    #region FillQueries
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

        self.cursor.execute("""
                            SELECT cntr, booking, status, freetime, armador, terminal, tara, expurgo
                            FROM CNTRs 
                            WHERE (booking LIKE ? AND cntr LIKE ? AND status LIKE ?)
                            """
                            , ('%' + str(booking) + '%', '%' + str(cntr) + '%', '%' + str(status) + '%',))
        
        result = self.cursor.fetchall()

        return result
    
    def FillViagensTable(self, cntr, booking, status, data, anyDate):

        if not (self.isDBopened):
            self.OpenDB()

        if (anyDate):
            self.cursor.execute("""
                                SELECT 
                                    Viagens.ID,
                                    Viagens.status,
                                    CNTRs.booking,
                                    CNTRs.cntr,
                                    Viagens.dataInicio,
                                    Viagens.dataFim,
                                    Viagens.cpfMotorista,
                                    Viagens.placaCavalo,
                                    Viagens.placaCarreta,
                                    Viagens.spot
                                FROM 
                                    CNTRs
                                INNER JOIN Viagens on Viagens.cntr = CNTRs.cntr
                                WHERE (CNTRs.booking LIKE ? AND CNTRs.cntr LIKE ? AND Viagens.status LIKE ?)
                                """
                                , ('%' + str(booking) + '%', '%' + str(cntr) + '%', '%' + str(status) + '%',))  
        
        else:
            self.cursor.execute("""
                                SELECT 
                                    Viagens.ID,
                                    Viagens.status,
                                    CNTRs.booking,
                                    CNTRs.cntr,
                                    Viagens.dataInicio,
                                    Viagens.dataFim,
                                    Viagens.cpfMotorista,
                                    Viagens.placaCavalo,
                                    Viagens.placaCarreta,
                                    Viagens.spot
                                FROM 
                                    CNTRs
                                INNER JOIN Viagens on Viagens.cntr = CNTRs.cntr
                                WHERE (CNTRs.booking LIKE ? AND CNTRs.cntr LIKE ? AND Viagens.status LIKE ? AND Viagens.dataInicio LIKE ?)
                                """
                                , ('%' + str(booking) + '%', '%' + str(cntr) + '%', '%' + str(status) + '%', '%' + str(data) + '%',))  
        
        result = self.cursor.fetchall()
        return result
    
    #endregion

    #region ListsSetup
    def GetArmadores(self):

        if not (self.isDBopened):
            self.OpenDB()
        
        self.cursor.execute("SELECT * FROM _Armadores ORDER BY armador")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data
    
    def GetFabricas(self):

        if not (self.isDBopened):
            self.OpenDB()
        
        self.cursor.execute("SELECT * FROM _Fabricas ORDER BY fabrica")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data
    
    def GetPortos(self):

        if not (self.isDBopened):
            self.OpenDB()
        
        self.cursor.execute("SELECT * FROM _Portos ORDER BY porto")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data
    
    def GetStatusCNTR(self):

        if not (self.isDBopened):
            self.OpenDB()
        
        self.cursor.execute("SELECT * FROM _StatusCNTR")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data
    
    def GetStatusPedido(self):

        if not (self.isDBopened):
            self.OpenDB()
        
        self.cursor.execute("SELECT * FROM _StatusPedido")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data
    
    def GetStatusViagem(self):

        if not (self.isDBopened):
            self.OpenDB()
        
        self.cursor.execute("SELECT * FROM _StatusViagem ORDER BY status")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data
    
    def GetTerminais(self):

        if not (self.isDBopened):
            self.OpenDB()
        
        self.cursor.execute("SELECT * FROM _Terminais ORDER BY terminal")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data

    def GetTipoViagem(self):

        if not (self.isDBopened):
            self.OpenDB()
        
        self.cursor.execute("SELECT * FROM _TipoViagem ORDER BY tipo")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data

    def GetCPF(self):

        if not (self.isDBopened):
            self.OpenDB()
        
        self.cursor.execute("SELECT CPF FROM _BancoConjunto ORDER BY CPF")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data
    
    def GetMotorista(self, cpf = ''):

        if not (self.isDBopened):
            self.OpenDB()
        
        if (cpf == ''):
            self.cursor.execute("SELECT motorista FROM _BancoConjunto")            
            result = self.cursor.fetchall()
            data = []
            for i in range(len(result)):
                data.append(str(result[i][0]))

            return data
        else:
            self.cursor.execute("SELECT motorista FROM _BancoConjunto WHERE CPF = ?",
                                (str(cpf),))
            result = self.cursor.fetchone()
            return result[0]
    
    def GetCavalo(self, cpf = ''):

        if not (self.isDBopened):
            self.OpenDB()
        
        if (cpf == ''):
            self.cursor.execute("SELECT placaCavalo FROM _BancoConjunto")            
            result = self.cursor.fetchall()
            data = []
            for i in range(len(result)):
                data.append(str(result[i][0]))

            return data
        else:
            self.cursor.execute("SELECT placaCavalo FROM _BancoConjunto WHERE CPF = ?",
                                (str(cpf),))
            result = self.cursor.fetchone()
            return result[0]
    
    def GetCarreta(self, cpf = ''):

        if not (self.isDBopened):
            self.OpenDB()
        
        if (cpf == ''):
            self.cursor.execute("SELECT placaCarreta FROM _BancoConjunto")
            result = self.cursor.fetchall()
            data = []
            for i in range(len(result)):
                data.append(str(result[i][0]))

            return data
        else:
            self.cursor.execute("SELECT placaCarreta FROM _BancoConjunto WHERE CPF = ?",
                                (str(cpf),))
            result = self.cursor.fetchone()
            return result[0]

    #endregion