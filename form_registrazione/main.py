import json          # Per gestire il formato JSON
import hashlib       # Per l'hashing delle password
import os            # Per verificare l'esistenza dei file
import tkinter as tk # Per l'interfaccia grafica
from tkinter import messagebox # Per mostrare messaggi all'utente

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

# Classe per l'interfaccia grafica
class AuthenticationApp:
    """
    Classe che gestisce l'interfaccia grafica del sistema di autenticazione.
    """
    def __init__(self, root):
        """
        Inizializza l'interfaccia grafica.
        
        Args:
            root: L'oggetto principale dell'interfaccia Tkinter
        """
        self.root = root
        self.root.title("Sistema di Autenticazione")  # Titolo della finestra
        self.root.geometry("400x300")  # Dimensione della finestra
        
        # Creazione del frame principale con padding
        self.main_frame = tk.Frame(root, padx=20, pady=20)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Etichetta titolo in alto
        self.title_label = tk.Label(self.main_frame, text="Sistema di Autenticazione", font=("Arial", 16))
        self.title_label.pack(pady=10)
        
        # Campo per inserire il nome utente
        self.username_frame = tk.Frame(self.main_frame)
        self.username_frame.pack(fill=tk.X, pady=5)
        
        self.username_label = tk.Label(self.username_frame, text="Nome utente:", width=12, anchor="w")
        self.username_label.pack(side=tk.LEFT)
        
        self.username_entry = tk.Entry(self.username_frame)
        self.username_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Campo per inserire la password (caratteri nascosti)
        self.password_frame = tk.Frame(self.main_frame)
        self.password_frame.pack(fill=tk.X, pady=5)
        
        self.password_label = tk.Label(self.password_frame, text="Password:", width=12, anchor="w")
        self.password_label.pack(side=tk.LEFT)
        
        self.password_entry = tk.Entry(self.password_frame, show="*")  # Il carattere "*" nasconde la password
        self.password_entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Pulsanti per registrazione e login
        self.buttons_frame = tk.Frame(self.main_frame)
        self.buttons_frame.pack(pady=20)
        
        self.register_button = tk.Button(self.buttons_frame, text="Registrati", command=self.register)
        self.register_button.pack(side=tk.LEFT, padx=10)
        
        self.login_button = tk.Button(self.buttons_frame, text="Accedi", command=self.login)
        self.login_button.pack(side=tk.LEFT, padx=10)
        
        # Area per visualizzare i messaggi di risultato
        self.message_label = tk.Label(self.main_frame, text="", font=("Arial", 12))
        self.message_label.pack(pady=10)
    
    def register(self):
        """
        Gestisce l'evento di click sul pulsante Registrati.
        Prende i dati inseriti dall'utente e tenta di registrarlo.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Verifica che i campi non siano vuoti
        if not username or not password:
            messagebox.showerror("Errore", "Nome utente e password sono richiesti")
            return
        
        # Tenta la registrazione e mostra un messaggio appropriato
        success, message = register_user(username, password)
        
        if success:
            messagebox.showinfo("Successo", message)
            # Pulisce i campi dopo una registrazione riuscita
            self.username_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Errore", message)
    
    def login(self):
        """
        Gestisce l'evento di click sul pulsante Accedi.
        Prende i dati inseriti dall'utente e tenta di autenticarlo.
        """
        username = self.username_entry.get()
        password = self.password_entry.get()
        
        # Verifica che i campi non siano vuoti
        if not username or not password:
            messagebox.showerror("Errore", "Nome utente e password sono richiesti")
            return
        
        # Tenta l'autenticazione
        success, message = authenticate_user(username, password)
        
        # Mostra il risultato nell'etichetta dei messaggi
        if success:
            self.message_label.config(text=message, fg="green")  # Verde per successo
        else:
            self.message_label.config(text=message, fg="red")    # Rosso per errore

# Funzione principale
def main():
    """
    Punto di ingresso principale dell'applicazione con interfaccia grafica.
    Crea il file dati se non esiste e avvia l'interfaccia Tkinter.
    """
    # Verificare se esiste il file JSON, altrimenti crearlo
    if not os.path.exists(DATA_FILE):
        save_data({"users": {}})
    
    # Creare l'applicazione Tkinter
    root = tk.Tk()
    app = AuthenticationApp(root)
    root.mainloop()  # Avvia il loop principale dell'interfaccia grafica

# Punto di ingresso del programma
if __name__ == "__main__":
    main()  # Avvia l'interfaccia grafica
