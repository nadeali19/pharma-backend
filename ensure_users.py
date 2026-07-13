from pymongo import MongoClient
from werkzeug.security import generate_password_hash

MONGO_URI = "mongodb+srv://nadeali:alinade1926@cluster0.hgwzx4r.mongodb.net/pharma_db?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
db = client['pharma_db']

initial_users = [{"u":"admin","p":"admin123","r":"admin"},{"u":"user1","p":"1234","r":"user"}]

for u in initial_users:
    existing = db.users.find_one({"u": u["u"]})
    if not existing:
        clean_u = u.copy()
        clean_u["p"] = generate_password_hash(clean_u["p"])
        db.users.insert_one(clean_u)
        print(f"Added missing default user: {u['u']}")
    else:
        print(f"User already exists: {u['u']}")
