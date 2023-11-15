from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import pandas as pd

uri = "mongodb+srv://admin:W176xRINyYUOZCKE@cluster0.r000trc.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["Cluster0"]
collection = db["Accl_Data"]
result = collection.delete_many({})


