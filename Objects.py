class Pedido(object):

    def __init__(self, _pedido, _booking, _status, _cabotagem, _Expurgo, _armador, 
                _fabrica, _porto, _DLfabrica, _DLporto, _cntrs = [], _terminal = None,
                _janelaInicio = None, _janelaFim = None):
        
        self.numero = _pedido
        self.status = _status
        self.booking = _booking
        self.armador = _armador
        self.fabrica = _fabrica
        self.porto = _porto
        self.DLfabrica = _DLfabrica
        self.DLporto = _DLporto
        self.cntrs = _cntrs
        self.terminal = _terminal
        self.janelaInicio = _janelaInicio
        self.janelaFim = _janelaFim
        self.cabotagem = _cabotagem
        self.expurgo = _Expurgo

class CNTR(object):

    def __init__(self, _cntr, _status, _bookingFantasma, 
                _tara, _bookingReal = None, _pesoBruto = None, _viagens = []):

        self.numero = _cntr
        self.status = _status
        self.bookingFantasma = _bookingFantasma
        self.tara = _tara
        self.bookingReal = _bookingReal
        self.pesoBruto = _pesoBruto
        self.viagens = _viagens

class Viagem(object):

    def __init__(self, _ID, _tipoViagem, _inicio, _fim, _origem, 
                _destino, _CPF, _motorista, _cavalo, _carreta):
        
        self.ID = _ID
        self.tipoViagem = _tipoViagem
        self.inicio = _inicio
        self.fim = _fim
        self.origem = _origem
        self.destino = _destino
        self.CPF = _CPF
        self.motorista = _motorista
        self.cavalo = _cavalo
        self.carreta = _carreta