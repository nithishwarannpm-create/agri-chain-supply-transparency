import os

from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv(
    "MONGO_URI",
    "mongodb://localhost:27017"
)

MONGO_DB_NAME = os.getenv(
    "MONGO_DB_NAME",
    "agri_supply_chain"
)

client = MongoClient(MONGO_URI)

db = client[MONGO_DB_NAME]

products_collection = db["products"]
users_collection = db["users"]
transactions_collection = db["transactions"]
ai_results_collection = db["ai_results"]
blockchain_records_collection = db["blockchain_records"]


def check_database_connection():
    try:
        client.admin.command("ping")
        return True
    except Exception:
        return False