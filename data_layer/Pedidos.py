from .MongoConnector import MongoConnector
from .RedisConnector import RedisConnector
from datetime import date


class Pedidos:
    def gerar(cliente_id, produto, quantidade):
        data_em_texto = date.today().strftime('%Y%m%d')
        contadorPedidosDoDia = str(
            RedisConnector.inc(data_em_texto)).rjust(15, '0')

        reg = {
            "cliente_id": cliente_id,
            "numero": data_em_texto + contadorPedidosDoDia,
            "produto": produto,
            "quantidade": quantidade
        }        
        MongoConnector.executeCommandOnChatBotDb(
            lambda db: db.pedido.insert_one(reg)
        )
        return reg["numero"]
    
    def get_5_ultimos(cliente_id):
        return MongoConnector.executeCommandOnChatBotDb(
            lambda db: db.pedido.find({"cliente_id": cliente_id}).sort([['_id', -1]] ).limit(5)
        )
        