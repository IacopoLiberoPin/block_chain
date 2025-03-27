# Sistema di Autenticazione con Python
# Questo script implementa un sistema di registrazione e autenticazione utenti
# con salvataggio delle credenziali in un file JSON e hashing delle password con SHA-256.
# L'interfaccia funziona esclusivamente a linea di comando.

import json          # Per gestire il formato JSON
import hashlib       # Per l'hashing delle password
import os            # Per verificare l'esistenza dei file

# Percorso del file JSON dove verranno salvati username e password
DATA_FILE = "data.json"

# Funzione per caricare i dati dal file JSON
def load_data():
    """
    Carica i dati utente dal file JSON.
    Se il file esiste, tenta di caricarlo.
    Se il file non esiste o è malformato, restituisce un dizionario vuoto.
    
    Returns:
        dict: Dizionario contenente gli utenti registrati e le loro password hashate
    """
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                # Se il file JSON è corrotto, restituisce un dizionario vuoto
                return {"users": {}}
    else:
        # Se il file non esiste, restituisce un dizionario vuoto
        return {"users": {}}

# Funzione per salvare i dati nel file JSON
def save_data(data):
    """
    Salva i dati degli utenti nel file JSON.
    
    Args:
        data (dict): Dizionario contenente gli utenti e le password da salvare
    """
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)  # Salva con formattazione per leggibilità

# Funzione per codificare la password con SHA-256
def hash_password(password):
    """
    Codifica una password in chiaro utilizzando l'algoritmo SHA-256.
    
    Args:
        password (str): La password in chiaro
        
    Returns:
        str: L'hash esadecimale della password
    """
    return hashlib.sha256(password.encode()).hexdigest()

# Funzione per registrare un nuovo utente
def register_user(username, password):
    """
    Registra un nuovo utente nel sistema.
    
    Args:
        username (str): Nome utente desiderato
        password (str): Password in chiaro
        
    Returns:
        tuple: (successo, messaggio) dove successo è un booleano
               e messaggio è una stringa informativa
    """
    data = load_data()
    
    # Verifica se l'utente esiste già
    if username in data["users"]:
        return False, "Nome utente già esistente"
    
    # Hash della password e salvataggio
    hashed_password = hash_password(password)
    data["users"][username] = hashed_password
    save_data(data)
    
    return True, "Registrazione completata con successo"

# Funzione per autenticare un utente
def authenticate_user(username, password):
    """
    Autentica un utente verificando username e password.
    
    Args:
        username (str): Nome utente
        password (str): Password in chiaro
        
    Returns:
        tuple: (successo, messaggio) dove successo è un booleano
               e messaggio è una stringa informativa o di benvenuto
    """
    data = load_data()
    
    # Verifica se l'utente esiste
    if username not in data["users"]:
        return False, "Nome utente non trovato"
    
    # Verifica la password
    hashed_password = hash_password(password)
    if data["users"][username] == hashed_password:
        return True, f"Benvenuto {username}"
    else:
        return False, "Password errata"

# Funzione principale
def main():
    """
    Versione testuale dell'applicazione che funziona nel terminale.
    """
    # Verificare se esiste il file JSON, altrimenti crearlo
    if not os.path.exists(DATA_FILE):
        save_data({"users": {}})
        
    print("=== Sistema di Autenticazione ===")
    while True:
        # Menu principale
        print("\n1. Registrazione")
        print("2. Accesso")
        print("3. Esci")
        choice = input("Scelta: ")
        
        if choice == "1":
            # Opzione di registrazione
            username = input("Nome utente: ")
            password = input("Password: ")
            success, message = register_user(username, password)
            print(message)
        
        elif choice == "2":
            # Opzione di login
            username = input("Nome utente: ")
            password = input("Password: ")
            success, message = authenticate_user(username, password)
            print(message)
        
        elif choice == "3":
            # Uscita dal programma
            break
        
        else:
            print("Scelta non valida")

# Punto di ingresso del programma
if __name__ == "__main__":
    main()  # Avvia la modalità terminale
