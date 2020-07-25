import redis
import time
import os
from pymongo import MongoClient
from bson.json_util import dumps
import logging
from data_layer.Produtos import *
from data_layer.Pedidos import *
from datetime import date

logger = logging.getLogger('TelegramBot')

actions_dict = {    
    'consultarProdutos':lambda parameters, return_var:{ return_var : consutar_produtos() } ,
    'gerarPedido':lambda parameters, return_var: gerar_pedido(parameters, return_var), 
    'listarUltimosPedidos':lambda parameters, return_var: listar_ultimos(parameters, return_var) 
}

def action_handler(action, parameters, return_var):
    return_values = {}
    if action in actions_dict:
        return_values = actions_dict[action](parameters, return_var)    
    return {
            'skills': {
                'main skill': {
                    'user_defined': return_values
                }
            }
        }

def gerar_pedido(parameters, return_var):
    return { return_var: Pedidos.gerar(parameters["cliente_id"], parameters["produto"], parameters["quantidade"]) }

def consutar_produtos():    
    prods = Produtos.listarNomes()
    return __formata_lista(prods)

def listar_ultimos(parameters, return_var):
        pedidos = Pedidos.get_5_ultimos(parameters["cliente_id"])
        descPedidos = [ str(p["quantidade"])+" "+("unidades" if int(p["quantidade"]) > 1  else  "unidade") + " de {0}".format(p["produto"]) for p in pedidos]
        return { return_var: __formata_lista(descPedidos) }

def __formata_lista(lista):
    if (len(lista) == 1):
        return lista[0]
    elif (len(lista) > 1):
        inic = lista[:-1]
        return ", \n".join(inic) + " e " + lista[-1]
    else:
        return ""