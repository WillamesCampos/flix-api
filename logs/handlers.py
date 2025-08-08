import logging

from pymongo import MongoClient


class BaseHandler(logging.Handler):
    pass


class MongoHandler(BaseHandler):
    def __init__(self, mongo_uri: str, db_name: str, collection: str) -> None:
        super().__init__()
        self.client = MongoClient(mongo_uri, serverSelectionTimeoutMS=5000, connectTimeoutMS=5000)
        self.collection = self.client[db_name][collection]

        try:
            # Executar uma simples operação de verificação
            self.client.admin.command('ping')  # Isso irá verificar se estamos conectados
            print('Conexão com MongoDB estabelecida com sucesso!')
        except Exception as e:
            print(f'Aviso: falha ao pingar o MongoDB na inicialização do handler: {e}')
            raise

    def emit(self, record):
        log_entry = self.format(record)
        data = {
            'level': record.levelname,
            'message': log_entry,
            'pathname': record.pathname,
            'lineno': record.lineno,
            'funcName': record.funcName,
            'created': record.created,
        }
        try:
            self.collection.insert_one(data)
        except Exception:
            pass


def create_mongo_handler(mongo_uri, db_name, collection):
    return MongoHandler(mongo_uri, db_name, collection)
