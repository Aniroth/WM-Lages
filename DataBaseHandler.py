from typing import TypeVar
import Pedidos
import CNTRs
import Viagens
import sqlite3

def SavePedido(pedido):

    data = (pedido.numero, pedido.status)
    print (data)