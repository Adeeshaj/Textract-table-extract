from pymongo import MongoClient
from config import DOCUMENT_STORE

client = MongoClient(DOCUMENT_STORE["DB_HOST"], DOCUMENT_STORE["DB_PORT"], connect=False)

class Claim:
    def __init__(self, file_name=None, file=None, textract_jobId = None):
        self.__file_name = file_name
        self.__file = file
        self.__textract_job_id = textract_job_id
    
    def save(self):
        db = client[DOCUMENT_STORE["DB_NAME"]]
        collection = db[DOCUMENT_STORE["COLLECTION_CLAIMS"]]

        try:
            unique_id = collection.save({
                "file_name": self.__file_name
                "file": self.__file
                "textract_job_id": self.__textract_job_id
            })
        except Exception as e:
            unique_id = None
            print (e)

        return unique_id
