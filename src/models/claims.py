from pymongo import MongoClient
from config.config import DOCUMENT_STORE

client = MongoClient(DOCUMENT_STORE["DB_HOST"], DOCUMENT_STORE["DB_PORT"], connect=False)

class Claim:
    def __init__(self, file_name=None, rooms=None, textract_job_id = None):
        self.__file_name = file_name
        self.__rooms = rooms
        self.__textract_job_id = textract_job_id
    
    def save(self):
        db = client[DOCUMENT_STORE["DB_NAME"]]
        collection = db[DOCUMENT_STORE["COLLECTION_CLAIMS"]]

        try:
            unique_id = collection.save({
                "file_name": self.__file_name,
                "rooms": self.__rooms,
                "textract_job_id": self.__textract_job_id
            })
        except Exception as e:
            unique_id = None
            print (e)

        return unique_id
