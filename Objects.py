class Pedido(object):

    def __init__(self, _pedido, _booking, _status, 
                _cabotagem, _Expurgo, _armador,_fabrica, 
                _porto, _DLfabrica, _DLporto, _janelaInicio, 
                _janelaFim, _terminal = ''):
        
        self.numero = _pedido
        self.status = _status
        self.booking = _booking
        self.armador = _armador
        self.fabrica = _fabrica
        self.porto = _porto
        self.DLfabrica = _DLfabrica
        self.DLporto = _DLporto
        self.terminal = _terminal
        self.janelaInicio = _janelaInicio
        self.janelaFim = _janelaFim
        self.cabotagem = _cabotagem
        self.expurgo = _Expurgo

class CNTR(object):

    def __init__(self, _cntr, _status, _booking, 
                _tara, _freeTime, _obs):

        self.numero = _cntr
        self.status = _status
        self.tara = _tara
        self.booking = _booking
        self.freeTime = _freeTime
        self.obs = _obs

class Viagem(object):

    def __init__(self, _ID, _cntr, _tipoViagem, _inicio, _fim, _origem, 
                _destino, _CPF, _motorista, _cavalo, _carreta):
        
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