import os
import json
import requests
import random
import openpyxl
import uuid
import b64uuid

def default_config():
    return {
            "uri": "http://10.0.64.108:4000",
            "systemid": "JP001",
            "cell": 2,
            "rows": 5,
            "cols": 4,
            "datadir_ordergroup": "./data/ordergroup",
            "datadir_preset": "./data/preset"
    }

def read_config(config_file):
    if os.path.isfile(config_file):
        with open(config_file, "r") as f:
            try:
                return json.load(f)
            except:
                return default_config()
    else:
        return default_config()

def write_config(dict):
    with open("config.json", "w") as f:
        json.dump(dict, f, indent=2)

def post_data(data, path):
    c = read_config("config.json")
    try:
        response = requests.post(
            f'{c["uri"]}{path}',
            json.dumps(data),
            headers={'Content-Type': 'application/json'},
            timeout=3.5
        )
        return response
    
    except requests.exceptions.RequestException as e:
        return e

def read_excel(infile):
    indata = list()
    wb = openpyxl.load_workbook(infile, read_only=True)
    ws = wb[wb.sheetnames[0]]
    
    for row in ws.rows:
            # preset mode

            if len(row) == 2:   
                indata.append([row[0].value, row[1].value.upper()])
            # ordergroup mode (expirationDate)
            elif len(row) > 4 and row[0].value and row[1].value and row[3].value:
                indata.append(
                    [
                        str(row[0].value).upper(),
                        str(row[1].value),
                        str(row[2].value),
                        str(row[3].value),
                        str(row[4].value),
                    ]
                )
    if len(indata) > 0:
        indata.pop(0)
    return indata

def generate_ordergroup_id():
    return str(uuid.uuid1()).replace("-", "")

def gen_b64uuid():
    return b64uuid.B64UUID().string

def generate_session_key():
    return str(random.randint(1000, 100000000))