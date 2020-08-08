import CNTRs
import Viagens

class Pedido(object):

    def __init__(self, _pedido, _status, _booking, _armador, _fabrica, _porto, _DLfabrica, _DLporto, _cntrs = [], _janelaInicio = None, _janelaFim = None, _cabotagem = False, _Expurgo = True):
        
        self.numero = _pedido
        self.status = _status
        self.booking = _booking
        self.armador = _armador
        self.fabrica = _fabrica
        self.porto = _porto
        self.DLfabrica = _DLfabrica
        self.DLporto = _DLporto
        self.cntrs = _cntrs
        self.janelaInicio = _janelaInicio
        self.janelaFim = _janelaFim
        self.cabotagem = _cabotagem
        self.expurgo = _Expurgo