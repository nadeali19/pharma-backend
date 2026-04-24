from pymongo import MongoClient
import sys

MONGO_URI = "mongodb+srv://nadeali:alinade1926@cluster0.hgwzx4r.mongodb.net/?appName=Cluster0"

try:
    print("Connecting to NEW MongoDB...")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    client.admin.command('ismaster')
    print("SUCCESS: Connected to the NEW MongoDB!")
except Exception as e:
    print(f"FAILED: {e}")
    sys.exit(1)
