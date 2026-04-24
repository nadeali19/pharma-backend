from pymongo import MongoClient
import sys

MONGO_URI = "mongodb+srv://nadeali426:Alinade1926@cluster0.wml3oa4.mongodb.net/?appName=Cluster0"

try:
    print("Connecting to MongoDB...")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    # The ismaster command is cheap and does not require auth.
    client.admin.command('ismaster')
    print("Successfully connected to MongoDB!")
except Exception as e:
    print(f"FAILED to connect to MongoDB: {e}")
    sys.exit(1)
