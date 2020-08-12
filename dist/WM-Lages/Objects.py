class Booking(object):

    def __init__(self, _booking, _status, 
                _cabotagem, _fabrica, _porto, _aPartir, 
                _DLporto, _qtde):
        
        self.status = _status
        self.booking = _booking
        self.fabrica = _fabrica
        self.porto = _porto
        self.aPartir = _aPartir
        self.DLporto = _DLporto
        self.cabotagem = _cabotagem
        self.qtde = _qtde

class CNTR(object):

    def __init__(self, _cntr, _status, _booking, 
                _tara, _armador, _terminal, _dataColeta, 
                _freeTime, _obs = '', _expurgo = 0, _oferta = '', _lacre = '', _agendamento = '', _dataAgendamento = ''):

        self.cntr = _cntr
        self.status = _status
        self.booking = _booking
        self.tara = _tara
        self.armador = _armador
        self.terminal = _terminal
        self.dataColeta = _dataColeta
        self.freeTime = _freeTime
        self.obs = _obs
        self.expurgo = _expurgo
        self.oferta = _oferta
        self.lacre = _lacre
        self.agendamento = _agendamento
        self.dataAgendamento = _dataAgendamento

class Viagem(object):

    def __init__(self, _status, _cntr, _tipoViagem, 
                _inicio, _fim, _origem, _destino, 
                _CPF, _motorista, _cavalo, _carreta, _spot, _carreta2 = '', _ID = None):
        
        self.ID = _ID
        self.status = _status
        self.cntr = _cntr
        self.tipoViagem = _tipoViagem
        self.inicio = _inicio
        self.fim = _fim
        self.origem = _origem
        self.destino = _destino
        self.CPF = _CPF
        self.motorista = _motorista
        self.cavalo = _cavalo
        self.carreta = _carreta
        self.carreta2 = _carreta2
        self.spot = _spot

class Oferta(object):
        
    def __init__(self, _booking, _oferta = '', _ID = ''):
        
        self.booking = _booking
        self.oferta = _oferta
        self.ID = _ID