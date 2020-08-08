from typing import TypeVar
import Pedidos
import CNTRs
import Viagens
import sqlite3

def SavePedido(pedido):

    for cntr in pedido.cntrs:
        cntrsSTR += cntr

    data = (pedido.numero, 0, pedido.booking, pedido.status, cntrsSTR, 
            pedido.cabotagem, pedido.expurgo, pedido.armador, pedido.armador, 
            pedido.origem, pedido.destino, pedido.DLfabrica, pedido.DLporto,
            pedido.janelaInicio, pedido.janelaFim)
    
    print (data)