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
    to_find = ""
    if blocks:
        block_id = blocks[-1]["block"]["id"] + 1
        prev_hash = blocks[-1]["block"]["hash"]
        nonce = blocks[-1]["block"]["nonce"]+1
        n=0
        xx=""
        while(n<nonce):
            xx=xx+"0"
    
        to_find =xx+blocks[-1]["block"]["hash"]        
    else:
        block_id = 0
        prev_hash = None
        nonce = 0
        to_find = "0"

    new_block = {
        "id": block_id,
        "prev_hash": prev_hash,
        "hash": hashlib.sha256(input_data.encode()).hexdigest(),
        "timestamp": dt.datetime.now().isoformat(),
        "data": input_data,
        "utente": utente,
        "nonce": nonce,
        "to_find": to_find
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
        
def mine():
    blocks = load_blocks()
    
    if not blocks:
        print("Nessun blocco da minare.")
        return
    
    last_block = blocks[-1]["block"]
    nonce = 0  # Start with 0 and increment
    difficulty = last_block.get("nonce", 0)
    
    # Create target pattern with required number of zeros
    target_pattern = '0' * difficulty
    
    print(f"Inizio mining con difficoltà {difficulty} (cercando {target_pattern} all'inizio del hash)...")
    
    while True:
        # Create a string to hash (combining block data with a nonce)
        data_to_hash = f"{last_block['hash']}{nonce}{last_block['data']}"
        
        # Calculate new hash
        new_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()
        
        # Check if hash starts with required number of zeros
        if new_hash.startswith(target_pattern):
            print(f"Mining completato! Trovato hash valido dopo {nonce} tentativi.")
            print(f"Hash trovato: {new_hash}")
            
            # Create new block with the mined data
            mined_block = {
                "id": last_block["id"] + 1,
                "prev_hash": last_block["hash"],
                "hash": new_hash,
                "timestamp": dt.datetime.now().isoformat(),
                "data": f"Blocco minato (nonce: {nonce})",
                "utente": "Miner",
                "nonce": difficulty + 1,  # Increase difficulty for next block
                "to_find": target_pattern + new_hash
            }
            
            blocks.append({"block": mined_block})
            save_data(blocks)
            return
        
        # Increment nonce and show progress periodically
        nonce += 1
        if nonce % 10000 == 0:
            print(f"Tentativo {nonce}... Ultimo hash: {new_hash}")