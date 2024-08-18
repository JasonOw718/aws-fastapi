from db.models import Base
from db.database import engine
from fastapi import FastAPI
from router import chatbot, initialize
from fastapi.middleware.cors import CORSMiddleware

from pymongo.mongo_client import MongoClient
import os
uri = os.getenv("MONGO_DB_URI")
    
app = FastAPI()
app.include_router(initialize.router)
app.include_router(chatbot.router)

client = MongoClient(uri)

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

origins = [
    os.getenv("API_URL")
]

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_headers = ["*"],
    allow_methods = ["*"],
    allow_credentials = True
)


Base.metadata.create_all(engine)

