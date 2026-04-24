from flask import Flask, jsonify, request, send_file
from pymongo import MongoClient
from flask_cors import CORS
import os
from datetime import datetime

app = Flask(__name__)
CORS(app)

# New Connection String
MONGO_URI = "mongodb+srv://nadeali:alinade1926@cluster0.hgwzx4r.mongodb.net/pharma_db?retryWrites=true&w=majority"
try:
    print("Connecting to MongoDB Atlas...")
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000, tlsAllowInvalidCertificates=True)
    # Trigger a connection to verify
    client.admin.command('ismaster')
    db = client['pharma_db']
    print("SUCCESS: Connected to MongoDB!")
    db_err = None
except Exception as e:
    db_err = str(e)
    print(f"CRITICAL ERROR: Could not connect to MongoDB: {db_err}")
    db = None # We will handle this in routes

initial_items = [
  {"id":"I001","name":"Paracetamol 500mg","salt":"Paracetamol","company":"Cipla","pack":"10T","rate":25,"mrp":30,"gst":5,"stock":500,"batches":[{"b":"B231","exp":"12/26","qty":200,"cost":18},{"b":"B241","exp":"06/27","qty":300,"cost":19}]},
  {"id":"I002","name":"Amoxicillin 250mg","salt":"Amoxicillin","company":"Ranbaxy","pack":"10C","rate":85,"mrp":100,"gst":12,"stock":200,"batches":[{"b":"C101","exp":"03/26","qty":100,"cost":60}]},
  {"id":"I003","name":"Metformin 500mg","salt":"Metformin HCl","company":"Sun Pharma","pack":"10T","rate":45,"mrp":55,"gst":5,"stock":350,"batches":[{"b":"M001","exp":"01/27","qty":350,"cost":32}]},
  {"id":"I004","name":"Atorvastatin 10mg","salt":"Atorvastatin","company":"Lupin","pack":"10T","rate":120,"mrp":145,"gst":12,"stock":150,"batches":[{"b":"A001","exp":"11/26","qty":150,"cost":88}]},
  {"id":"I005","name":"Pantoprazole 40mg","salt":"Pantoprazole","company":"USV","pack":"10T","rate":95,"mrp":115,"gst":5,"stock":280,"batches":[{"b":"P001","exp":"08/27","qty":280,"cost":70}]},
  {"id":"I006","name":"Azithromycin 500mg","salt":"Azithromycin","company":"Cipla","pack":"3T","rate":180,"mrp":220,"gst":12,"stock":90,"batches":[{"b":"Z001","exp":"05/26","qty":90,"cost":130}]},
  {"id":"I007","name":"Cetirizine 10mg","salt":"Cetirizine HCl","company":"GSK","pack":"10T","rate":35,"mrp":42,"gst":5,"stock":400,"batches":[{"b":"CE01","exp":"02/27","qty":400,"cost":25}]},
  {"id":"I008","name":"Omeprazole 20mg","salt":"Omeprazole","company":"Torrent","pack":"10C","rate":60,"mrp":75,"gst":5,"stock":320,"batches":[{"b":"OM01","exp":"07/27","qty":320,"cost":44}]},
  {"id":"I009","name":"Metronidazole 400mg","salt":"Metronidazole","company":"Cipla","pack":"10T","rate":28,"mrp":35,"gst":5,"stock":180,"batches":[{"b":"MT01","exp":"04/26","qty":80,"cost":18}]},
  {"id":"I010","name":"Amlodipine 5mg","salt":"Amlodipine","company":"Zydus","pack":"10T","rate":55,"mrp":68,"gst":5,"stock":260,"batches":[{"b":"AM01","exp":"06/27","qty":260,"cost":40}]},
]

initial_users = [{"u":"admin","p":"admin123","r":"admin"},{"u":"user1","p":"1234","r":"user"}]
initial_parties = [{"name":"Medico Suppliers","type":"Supplier","bal":15000},{"name":"City General Hospital","type":"Customer","bal":-2300},{"name":"Health Distributor","type":"Supplier","bal":8500}]

def initialize_db():
    if db is None:
        print("Skipping DB Init: Connection not available")
        return
    try:
        if db.items.count_documents({}) == 0:
            db.items.insert_many(initial_items)
            print("Initialized default items in DB")
        if db.users.count_documents({}) == 0:
            db.users.insert_many(initial_users)
            print("Initialized default users in DB")
        if db.parties.count_documents({}) == 0:
            db.parties.insert_many(initial_parties)
            print("Initialized default parties in DB")
    except Exception as e:
        print(f"Error during DB Initialization: {e}")


def sterilize(doc):
    if isinstance(doc, list):
        return [sterilize(x) for x in doc]
    if isinstance(doc, dict):
        new_doc = {}
        for k, v in doc.items():
            if k == '_id':
                new_doc[k] = str(v)
            elif isinstance(v, (datetime, bytes)):
                new_doc[k] = str(v)
            elif isinstance(v, (dict, list)):
                new_doc[k] = sterilize(v)
            else:
                new_doc[k] = v
        return new_doc
    return doc

# Run initialization once on startup
initialize_db()

@app.route('/')
def serve_index():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    target = os.path.join(base_dir, 'marg_pharma.html')
    print(f"Serving: {target}")
    if not os.path.exists(target):
        return f"Error: {target} not found!", 404
    return send_file(target)

@app.route('/api/data', methods=['GET'])
def get_data():
    if db is None:
        return jsonify({"error": "Database not connected", "details": db_err}), 503
    try:
        items = sterilize(list(db.items.find({})))
        bills = sterilize(list(db.bills.find({})))
        users = sterilize(list(db.users.find({})))
        parties = sterilize(list(db.parties.find({})))
        profile = sterilize(db.profile.find_one({}))
        return jsonify({"items": items, "bills": bills, "users": users, "parties": parties, "profile": profile})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/saveProfile', methods=['POST'])
def save_profile():
    if db is None:
        return jsonify({"error": "Database not connected"}), 503
    try:
        data = request.json
        profile = data.get('profile')
        if not profile:
            return jsonify({"error": "Missing profile data"}), 400
        
        db.profile.update_one({}, {"$set": profile}, upsert=True)
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/saveBill', methods=['POST'])
def save_bill():
    if db is None:
        return jsonify({"error": "Database not connected"}), 503
    try:
        data = request.json
        bill = data.get('bill')
        bill_delete = data.get('bill_delete')
        updated_items = data.get('items')
        updated_party = data.get('party')
        
        if not updated_items:
            return jsonify({"error": "Missing items data"}), 400

        # Handle Bill Deletion (Return)
        if bill_delete:
            db.bills.delete_one({"no": bill_delete})
        
        # Handle Bill Insertion
        if bill:
            db.bills.insert_one(bill)
        
        # Update stock for items
        for item in updated_items:
            db.items.update_one(
                {"id": item["id"]},
                {"$set": {"stock": item["stock"]}}
            )
        
        # Update party if provided
        if updated_party:
            db.parties.update_one(
                {"name": updated_party["name"]},
                {"$set": {
                    "bal": updated_party["bal"],
                    "transactions": updated_party.get("transactions", [])
                }},
                upsert=True
            )
            
        return jsonify({"success": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
