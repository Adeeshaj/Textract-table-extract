from pymongo import MongoClient
from config.config import DOCUMENT_STORE
import datetime

client = MongoClient(DOCUMENT_STORE["DB_HOST"], DOCUMENT_STORE["DB_PORT"], connect=False)

class Output:
    def __init__(self, file_name=None, table=None, file_path=None, textract_job_id = None):
        self.__file_name = file_name
        self.__file_path = file_path
        self.__table = table
        self.__textract_job_id = textract_job_id
        
    
    def save(self):
        db = client[DOCUMENT_STORE["DB_NAME"]]
        collection = db[DOCUMENT_STORE["COLLECTION_OUTPUTS"]]

        try:
            unique_id = collection.save({
                "file_name": self.__file_name,
                "file_path": self.__file_path,
                "textract_job_id": self.__textract_job_id,
                "table": self.__table,
                "createdAt": datetime.datetime.utcnow(),
                "updatedAt": datetime.datetime.utcnow()
            })
        except Exception as e:
            unique_id = None
            print (e)

        return unique_id


    def get_table(self):
        return self.__table