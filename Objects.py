class Pedido(object):

    def __init__(self, _pedido, _booking, _status, 
                _cabotagem, _fabrica, _porto, _DLfabrica, 
                _DLporto, _janelaInicio, _janelaFim):
        
        self.pedido = _pedido
        self.status = _status
        self.booking = _booking
        self.fabrica = _fabrica
        self.porto = _porto
        self.DLfabrica = _DLfabrica
        self.DLporto = _DLporto
        self.janelaInicio = _janelaInicio
        self.janelaFim = _janelaFim
        self.cabotagem = _cabotagem

class CNTR(object):

    def __init__(self, _cntr, _status, _booking, 
                _tara, _armador, _terminal, _dataColeta, 
                _freeTime, _obs = '', _expurgo = 0):

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

class Viagem(object):

    def __init__(self, _ID, _cntr, _tipoViagem, 
                _inicio, _fim, _origem, _destino, 
                _CPF, _motorista, _cavalo, _carreta):
        
        self.ID = _ID
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