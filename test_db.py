from pymongo import MongoClient
import os

uri = os.getenv("MONGODB_URI")
client = MongoClient(uri)
db = client["pawmatch"]

print("Databases:", client.list_database_names())
print("Collections in pawmatch:", db.list_collection_names())
