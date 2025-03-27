import os
import datetime as dt
import hashlib
from block import * 

DATA_FILE = "./blocks.json"

def main():
    if not os.path.exists(DATA_FILE):        
        save_data({"block": {
            "id": 0,
            "prev_hash": None,
            "hash":hashlib.sha256("blocco genesis".encode()).hexdigest(),
            "timestamp":dt.datetime.now().isoformat(),
            "data":"blocco genesis",
            "utente":None
        }})
    
    print("Benvenuto nel sistema di gestione dei blocchi.")
    while True:
        print("\n1. Aggiungi un nuovo blocco")
        print("2. Visualizza i blocchi esistenti")
        print("3. Esci")
        choice = input("Scegli un'opzione: ")

        if choice == "1":
            new_block()
        elif choice == "2":
            view_blocks()
        elif choice == "3":
            break
        else:
            print("Opzione non valida. Riprova.")


        
if __name__ == "__main__":
    main()