import Viagens

class CNTR(object):

    def __init__(self, _cntr, _status, _bookingFantasma, _tara, _bookingReal = None, _pesoBruto = None, _viagens = []):

        self.numero = _cntr
        self.status = _status
        self.bookingFantasma = _bookingFantasma
        self.tara = _tara
        self.bookingReal = _bookingReal
        self.pesoBruto = _pesoBruto
        self.viagens = _viagens