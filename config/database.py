from pymongo import MongoClient

client = MongoClient("mongodb+srv://kashengow:VgBNULFXFxEIyrwn@cluster0.s8hgq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

db = client.chat_db

collection_name = db["chat_collection"]