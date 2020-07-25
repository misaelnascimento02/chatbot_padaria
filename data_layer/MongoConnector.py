import os
from pymongo import MongoClient
from pymongo.database import Database
from pymongo.database import Database
from typing import Callable
import logging

logger = logging.getLogger('TelegramBot')

class MongoConnector:
    def executeCommandOnChatBotDb(cmd:Callable[[Database], any]):
        urlDb = 'mongodb://' + os.environ['MONGODB_USERNAME'] + ':' + \
            os.environ['MONGODB_PASSWORD'] + '@' + \
                os.environ['MONGODB_HOSTNAME'] + ':'+os.environ['MONGODB_PORT']+'/'
        mongo = MongoClient(urlDb)
        db = mongo[os.environ['MONGODB_DATABASE']]
        try:
            return cmd(db)
        except:
            logger.error('falha ao executar comando na base de dados!')    
        mongo.close()


