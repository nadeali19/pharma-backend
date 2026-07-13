from pymongo import MongoClient
from werkzeug.security import generate_password_hash

MONGO_URI = "mongodb+srv://nadeali:alinade1926@cluster0.hgwzx4r.mongodb.net/pharma_db?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
db = client['pharma_db']

users = list(db.users.find({}))
print("Re-hashing plain text passwords...")
for u in users:
    p = u.get('p', '')
    if p and ":" not in p:
        hashed_p = generate_password_hash(p)
        db.users.update_one({"_id": u["_id"]}, {"$set": {"p": hashed_p}})
        print(f"Hashed password for user: {u.get('u')}")
print("Done.")
