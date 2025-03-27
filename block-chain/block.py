import json
import datetime as dt
import hashlib

DATA_FILE = "./blocks.json"

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=5)



def load_blocks():
    """Load blocks from the JSON file and handle different formats."""
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
            
            if isinstance(data, dict) and "block" in data:
                return [data]  # Convert single block to list format
            elif isinstance(data, list):
                return data
            else:
                return []
    except (FileNotFoundError, json.JSONDecodeError):
        return []



def new_block():
    utente = input("Inserisci il nome utente: ")
    input_data = input("Inserisci i dati del blocco: ")
    
    blocks = load_blocks()

    # Get the ID and hash of the last block, if any
    if blocks:
        block_id = blocks[-1]["block"]["id"] + 1
        prev_hash = blocks[-1]["block"]["hash"]
    else:
        block_id = 0
        prev_hash = None

    new_block = {
        "id": block_id,
        "prev_hash": prev_hash,
        "hash": hashlib.sha256(input_data.encode()).hexdigest(),
        "timestamp": dt.datetime.now().isoformat(),
        "data": input_data,
        "utente": utente
    }

    blocks.append({"block": new_block})
    save_data(blocks)



def view_blocks():
    blocks = load_blocks()
    
    if not blocks:
        print("Nessun blocco trovato.")
        return
        
    for block in blocks:
        print(f"ID: {block['block']['id']}, "
              f"Hash: {block['block']['hash']}, "
              f"Timestamp: {block['block']['timestamp']}, "
              f"Data: {block['block']['data']}, "
              f"Utente: {block['block']['utente']}")