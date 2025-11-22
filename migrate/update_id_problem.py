#!/usr/bin/env python3
"""
Script to migrate and add MongoDB _id to JSONL file
"""

import json
from pymongo import MongoClient
import os
from dotenv import load_dotenv

# MongoDB connection
load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = "problems"

# Files
INPUT_JSONL = "data/problem_solution_data.jsonl"
OUTPUT_JSONL = "data/problem_solution_data_v1.jsonl"

def migrate_ids():
    # Connect to MongoDB
    client = MongoClient(MONGO_URI)
    db = client[DATABASE_NAME]
    collection = db[COLLECTION_NAME]
    
    # Read and process JSONL
    with open(INPUT_JSONL, 'r', encoding='utf-8') as fin, \
         open(OUTPUT_JSONL, 'w', encoding='utf-8') as fout:
        
        for line_num, line in enumerate(fin, 1):
            try:
                # Parse JSON line
                data = json.loads(line.strip())
                
                # Get name from JSONL
                name = data.get('name')
                if not name:
                    print(f"⚠️  Line {line_num}: No 'name' field found")
                    continue
                
                # Find in MongoDB
                mongo_doc = collection.find_one({'name': name})
                
                if mongo_doc:
                    # Add _id to data
                    data['_id'] = str(mongo_doc['_id'])
                    print(f"✅ Line {line_num}: {name} -> {data['_id']}")
                else:
                    print(f"❌ Line {line_num}: {name} not found in MongoDB")
                
                # Write to output
                fout.write(json.dumps(data, ensure_ascii=False) + '\n')
                
            except Exception as e:
                print(f"❌ Error at line {line_num}: {e}")
    
    client.close()
    print("\n✅ Migration completed!")

if __name__ == '__main__':
    migrate_ids()