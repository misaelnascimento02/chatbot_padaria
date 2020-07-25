from .MongoConnector import MongoConnector
class Produtos:
    def listarNomes():
        return MongoConnector.executeCommandOnChatBotDb(
            lambda db: list([p['nome'] for p in db.produtos.find()])
        )
