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

    conn = sqlite3.connect('BancoDeDados\\Banco de Dados.db')
    cursor = conn.cursor()

    #region SaveQueries
    def NewOferta(self, oferta, qtde):

        dataStream = []
        for i in range(qtde):
            dataStream.append((
                             None,
                             oferta.oferta,
                             oferta.booking
                             ))
        
        self.cursor.executemany("INSERT INTO Ofertas VALUES (?, ?, ?)", dataStream)
        self.conn.commit()
    
    def SaveBooking(self, booking):

        dataStream = ( 
                      1, 
                      booking.booking, 
                      booking.status, 
                      booking.cabotagem, 
                      booking.fabrica, 
                      booking.porto, 
                      booking.DLfabrica, 
                      booking.DLporto,
                      booking.janelaInicio, 
                      booking.janelaFim,
                      booking.qtde
                      )

        self.cursor.execute("INSERT OR REPLACE INTO Bookings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", dataStream)
        self.conn.commit()

    def SaveCNTR(self, CNTR):

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

        dataStream = (
                      None,
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

        self.cursor.execute("INSERT OR REPLACE INTO Viagens VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", dataStream)
        self.conn.commit()
    #endregion

    #region LoadQueries
    def OpenBooking(self, booking):
    
        self.cursor.execute("""
                            SELECT * FROM Bookings
                            WHERE booking LIKE ?
                            """, ('%' + str(booking) + '%',))            


        dataStream = self.cursor.fetchone()

        return dataStream
    
    def OpenCNTR(self, cntr):

        self.cursor.execute("""
                            SELECT * FROM CNTRs
                            WHERE cntr = ?
                            """, (str(cntr),))
        
        dataStream = self.cursor.fetchone()

        return dataStream
    #endregion

    #region DeleteQueries
    def DeleteBooking(self, booking):
        
        self.cursor.execute("""
                            DELETE FROM Bookings
                            WHERE booking = ?
                            """, (str(booking),))
        
        self.conn.commit()
    
    def DeleteCNTR(self, cntr):
        
        self.cursor.execute("""
                            DELETE FROM CNTRs
                            WHERE cntr= ?
                            """, (str(cntr),))
        
        self.conn.commit()

    #endregion

    #region FillQueries
    def FillBookingSearch(self, valueSeach):

        self.cursor.execute("""
                            SELECT booking, status, deadlinePorto 
                            FROM Bookings
                            WHERE booking LIKE ?"""
                            , ('%' + str(valueSeach) + '%',))
        
        result = self.cursor.fetchall()

        return result
    
    def FillBookingTable(self, booking):

        self.cursor.execute("""
                            SELECT
                                Ofertas.ID,
                                Ofertas.oferta,
                                CNTRs.cntr, 
                                CNTRs.status, 
                                CNTRs.tara, 
                                CNTRs.terminal, 
                                CNTRs.armador,
                                Viagens.cpfMotorista,
                                Viagens.nomeMotorista,
                                Viagens.placaCavalo,
                                Viagens.placaCarreta,
                                CNTRs.expurgo
                            FROM 
                                Ofertas
                            LEFT JOIN CNTRs ON CNTRs.oferta = Ofertas.oferta
                            LEFT JOIN Viagens on CNTRs.cntr = Viagens.cntr
                            WHERE Ofertas.booking = ?
                            GROUP BY Ofertas.ID
                            ORDER BY Ofertas.ID ASC
                            """
                            , (str(booking),))
        
        result = self.cursor.fetchall()

        return result
    
    def FillCNTRTable(self, booking, cntr, status):

        self.cursor.execute("""
                            SELECT 
                                CNTRs.cntr, 
                                CNTRs.booking, 
                                CNTRs.status, 
                                CNTRs.freetime, 
                                CNTRs.armador, 
                                CNTRs.terminal, 
                                CNTRs.tara, 
                                CNTRs.expurgo,
                                Viagens.cpfMotorista,
                                Viagens.nomeMotorista,
                                Viagens.placaCavalo,
                                Viagens.placaCarreta,
                                CNTRs.obs
                            FROM 
                                CNTRs
                            INNER JOIN Viagens on Viagens.cntr = CNTRs.cntr 
                            WHERE (CNTRs.booking LIKE ? AND CNTRs.cntr LIKE ? AND CNTRs.status LIKE ?)
                            """
                            , ('%' + str(booking) + '%', '%' + str(cntr) + '%', '%' + str(status) + '%',))
        
        result = self.cursor.fetchall()

        return result
    
    def FillViagensTable(self, cntr, booking, status, data, anyDate):

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
        
        self.cursor.execute("SELECT * FROM _Armadores ORDER BY armador")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data
    
    def GetFabricas(self):
        
        self.cursor.execute("SELECT * FROM _Fabricas ORDER BY fabrica")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data
    
    def GetPortos(self):
        
        self.cursor.execute("SELECT * FROM _Portos ORDER BY porto")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data
    
    def GetStatusCNTR(self):
        
        self.cursor.execute("SELECT * FROM _StatusCNTR")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data
    
    def GetStatusPedido(self):
        
        self.cursor.execute("SELECT * FROM _StatusPedido")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data
    
    def GetStatusViagem(self):
        
        self.cursor.execute("SELECT * FROM _StatusViagem ORDER BY status")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data
    
    def GetTerminais(self):
        
        self.cursor.execute("SELECT * FROM _Terminais ORDER BY terminal")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data

    def GetTipoViagem(self):
        
        self.cursor.execute("SELECT * FROM _TipoViagem ORDER BY tipo")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data

    def GetCPF(self):
        
        self.cursor.execute("SELECT CPF FROM _BancoConjunto ORDER BY CPF")
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))

        return data
    
    def GetMotorista(self, cpf = ''):
        
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