from pymongo import MongoClient

MONGO_URI = "mongodb+srv://nadeali:alinade1926@cluster0.hgwzx4r.mongodb.net/pharma_db?retryWrites=true&w=majority"
client = MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)
db = client['pharma_db']

users = list(db.users.find({}))
print("--- Current Users in DB ---")
for u in users:
    p = u.get('p')
    r = u.get('r')
    is_hashed = ":" in p if isinstance(p, str) else False
    print(f"Username: '{u.get('u')}', Role: '{r}', Password: '{p}', Is Hashed: {is_hashed}")
print("---------------------------")


# Check for any user with 'staff' in username or role
staff_users = list(db.users.find({"$or": [{"u": {"$regex": "staff", "$options": "i"}}, {"r": {"$regex": "staff", "$options": "i"}}]}))
if staff_users:
    print("--- Staff-related Users ---")
    for u in staff_users:
        print(f"Username: '{u.get('u')}', Role: '{u.get('r')}'")
else:
    print("No users found with 'staff' in username or role.")

