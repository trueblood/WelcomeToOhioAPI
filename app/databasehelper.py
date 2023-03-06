import json
from pymongo_get_database import get_database
dbname = get_database()
collection_name = dbname["brother"]

class DatabaseHelper():
    # write to database
    def writeToDatabase(id, vin):   
        item = {
                "id": id,
                "vin": str(vin)
            }   
        collection_name.insert_one(item)

