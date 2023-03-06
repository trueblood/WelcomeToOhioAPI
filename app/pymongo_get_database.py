import os
from pymongo import MongoClient
from dotenv import load_dotenv


def get_database():
   load_dotenv()
   db_username = 'brother'
   db_password = 'BeNqWDZX4CtzbIlm'

   # Provide the mongodb atlas url to connect python to mongodb using pymongo
   CONNECTION_STRING = f"mongodb+srv://{db_username}:{db_password}@clusterzone.qvfg7gm.mongodb.net/test"
 
   # Create a connection using MongoClient. You can import MongoClient or use pymongo.MongoClient
   client = MongoClient(CONNECTION_STRING)
 
   # Create the database for our example (we will use the same database throughout the tutorial
   return client['brother']
  
# This is added so that many files can reuse the function get_database()
if __name__ == "__main__":   
  
   # Get the database
   dbname = get_database()