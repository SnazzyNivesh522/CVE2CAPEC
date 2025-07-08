from database import get_session
import os
import json


async def initialize_database():
    client = get_session()
    db = client["cve-attack"]
    collection = db["mappings"]

    for filename in os.listdir("database"):
        if filename.endswith(".jsonl"):
            with open(os.path.join("database", filename), "r") as file:
                for line in file:
                    doc = json.loads(line)
                    new_doc = {}
                    for cve_id, detail in doc.items():
                        new_doc["cve_id"] = cve_id
                        new_doc["cwe"] = detail["CWE"]
                        new_doc["capec"] = detail["CAPEC"]
                        new_doc["technique"] = detail["TECHNIQUES"]

                    await collection.insert_one(new_doc)
    print("Database initialized with mappings from JSONL files.")

    return db


async def update_new_cves():
    client = get_session()
    db = client["cve-attack"]
    collection = db["mappings"]
    with open("results/new_cves.jsonl", "r") as file:
        for line in file:
            doc = json.loads(line)
            new_doc = {}
            for cve_id, detail in doc.items():
                new_doc["cve_id"] = cve_id
                new_doc["cwe"] = detail["CWE"]
                new_doc["capec"] = detail["CAPEC"]
                new_doc["technique"] = detail["TECHNIQUES"]
            await collection.update_one(
                {"cve_id": new_doc["cve_id"]}, {"$set": new_doc}, upsert=True
            )
            print(f"Updated or inserted CVE: {new_doc['cve_id']}")
    print("New CVEs updated in the database.")

if __name__ == "__main__":
    import asyncio

    asyncio.run(initialize_database())
    asyncio.run(update_new_cves())
