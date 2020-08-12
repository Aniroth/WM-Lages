from Objects import *
import sqlite3
import xlwings

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

    #region NewCalls
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
    #endregion

    #region SaveQueries    
    def SaveOfertas(self, ofertas):
        
        dataStream = []
        for i in range(len(ofertas)):
            dataStream.append((ofertas[i].ID,
                               ofertas[i].oferta,
                               ofertas[i].booking))
        
        self.cursor.executemany("INSERT OR REPLACE INTO Ofertas VALUES (?, ?, ?)", dataStream)
        self.conn.commit()

    def SaveBooking(self, booking):

        dataStream = ( 
                      1, 
                      booking.booking, 
                      booking.status, 
                      booking.cabotagem, 
                      booking.fabrica, 
                      booking.porto, 
                      booking.aPartir, 
                      booking.DLporto,
                      booking.qtde
                      )

        self.cursor.execute("INSERT OR REPLACE INTO Bookings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", dataStream)
        self.conn.commit()

    def SaveCNTR(self, CNTR):

        dataStream = (
                      0,
                      CNTR.cntr,
                      CNTR.oferta,
                      CNTR.status,
                      CNTR.booking,
                      CNTR.tara,
                      CNTR.armador,
                      CNTR.terminal,
                      CNTR.dataColeta,
                      CNTR.freeTime,
                      CNTR.obs,
                      CNTR.expurgo,
                      CNTR.lacre,
                      CNTR.agendamento,
                      CNTR.dataAgendamento
                     )
        
        self.cursor.execute("INSERT OR REPLACE INTO CNTRs VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", dataStream)
        self.conn.commit()
        
    def SaveViagem(self, Viagem):

        dataStream = (
                      0,
                      Viagem.ID,
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
                      Viagem.carreta2,
                      Viagem.spot
                      )

        self.cursor.execute("INSERT OR REPLACE INTO Viagens VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", dataStream)
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
    
    def OpenViagem(self, viagem):
        
        self.cursor.execute("""
                            SELECT * FROM Viagens
                            WHERE ID = ?
                            """, (str(viagem),))
        
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
                                CNTRs.lacre,
                                CNTRs.terminal, 
                                CNTRs.armador,
                                CNTRs.expurgo,
                                CNTRs.obs
                            FROM 
                                Ofertas
                            LEFT JOIN CNTRs ON CNTRs.oferta = Ofertas.oferta
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
                                CNTRs.lacre,
                                CNTRs.expurgo,
                                CNTRs.obs
                            FROM 
                                CNTRs
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
                                    Viagens.origem,
                                    Viagens.destino,
                                    CNTRs.lacre,
                                    Viagens.cpfMotorista,
                                    Viagens.nomeMotorista,
                                    Viagens.placaCavalo,
                                    Viagens.placaCarreta,
                                    Viagens.placaCarreta2,
                                    Viagens.spot
                                FROM 
                                    CNTRs
                                LEFT JOIN Viagens on Viagens.cntr = CNTRs.cntr
                                WHERE (CNTRs.booking LIKE ? AND CNTRs.cntr LIKE ? AND Viagens.tipoViagem LIKE ?)
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
                                    Viagens.origem,
                                    Viagens.destino,
                                    CNTRs.lacre,
                                    Viagens.cpfMotorista,
                                    Viagens.nomeMotorista,
                                    Viagens.placaCavalo,
                                    Viagens.placaCarreta,
                                    Viagens.placaCarreta2,
                                    Viagens.spot
                                FROM 
                                    CNTRs
                                LEFT JOIN Viagens on Viagens.cntr = CNTRs.cntr
                                WHERE (CNTRs.booking LIKE ? AND CNTRs.cntr LIKE ? AND Viagens.tipoViagem LIKE ? AND Viagens.dataInicio LIKE ?)
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

    def GetFabrica(self, booking):

        self.cursor.execute("SELECT fabrica FROM Bookings WHERE booking = ?", (str(booking),))
        result = self.cursor.fetchone()
        data = str(result[0])

        return data

    def GetPorto(self, booking):

        self.cursor.execute("SELECT porto FROM Bookings WHERE booking = ?", (str(booking),))
        result = self.cursor.fetchone()
        data = str(result[0])

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

    def GetCPFs(self):
        
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

    def GetCarreta2(self, cpf = ''):
        
        if (cpf == ''):
            self.cursor.execute("SELECT placaCarreta2 FROM _BancoConjunto")
            result = self.cursor.fetchall()
            data = []
            data.append('')
            for i in range(len(result)):
                if (result[i][0] == ''):
                    continue
                data.append(str(result[i][0]))

            return data
        else:
            self.cursor.execute("SELECT placaCarreta2 FROM _BancoConjunto WHERE CPF = ?",
                                (str(cpf),))
            result = self.cursor.fetchone()
            return result[0]
    
    def Agendamentos(self, porto):
        self.cursor.execute("SELECT horario FROM _Agendamentos WHERE porto = ?",
                            (str(porto),))
        result = self.cursor.fetchall()
        data = []
        for i in range(len(result)):
            data.append(str(result[i][0]))
        
        return data

    def GetVersion(self):

        self.cursor.execute("SELECT ver FROM _Parametros")
        result = self.cursor.fetchone()
        data = str(result[0])

        return data
    #endregion

    def UpdateDataBase(self):
        
        app = xlwings.App(visible=False)
        workbook = app.books.open('BancoManual.xlsx')
        sheet = workbook.sheets[0]
        lastRow = sheet.range('A' + str(sheet.cells.last_cell.row)).end('up').row

        data = []
        for i in range(2, lastRow):
            if (sheet.range('E' + str(i)).value == None):
                carreta2 = ''
            else:
                carreta2 = str(sheet.range('E' + str(i)).value)
            
            data.append((str(sheet.range('A' + str(i)).value)[0:11],
                        str(sheet.range('B' + str(i)).value),
                        str(sheet.range('C' + str(i)).value),
                        str(sheet.range('D' + str(i)).value),
                        carreta2
                        ))
        
        self.cursor.executemany("""
                                INSERT OR REPLACE INTO _BancoConjunto
                                VALUES (?, ?, ?, ?, ?)
                                """, (data))
        
        self.conn.commit()
        workbook.save()
        workbook.close()
        app.quit()
