from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
from contextlib import contextmanager
import os

class MongoDB:
    def __init__(self):
        self.client = MongoClient(
            host=os.getenv("MONGO_HOST", "mongodb"),
            port=int(os.getenv("MONGO_PORT", 27017)),
            username=os.getenv("MONGO_USER", "root"),
            password=os.getenv("MONGO_PASSWORD", "rootpassword"),
            authSource="admin",
            authMechanism="SCRAM-SHA-256"
        )
        self.db = self.client["honeypot"]
        self._verify_connection()
    
    def _verify_connection(self):
        try:
            self.client.admin.command("ping")
        except ConnectionFailure:
            raise Exception("MongoDB connection failed")
    
    @contextmanager
    def session(self):
        try:
            yield self.db["sessions"]
        finally:
            pass  

    @contextmanager
    def commands(self):
        try:
            yield self.db["commands"]
        finally:
            pass
