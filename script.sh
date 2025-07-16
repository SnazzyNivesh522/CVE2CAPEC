source .venv/bin/activate

python3 update_capec_db.py
python3 update_cwe_db.py
python3 update_technique_db.py
python3 retrieve_cve.py
python3 cve2cwe.py
python3 cwe2capec.py
python3 capec2technique.py

python3 update_database.py

deactivate
