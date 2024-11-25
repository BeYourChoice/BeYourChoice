import os
from pymongo import MongoClient

class MaterialeDidattico:
    def __init__(self, db_url="mongodb+srv://rcione3:rcione3@beyourchoice.yqzo6.mongodb.net/", db_name="BeYourChoice"):
        self.client = MongoClient(db_url)
        self.db = self.client[db_name]
        self.materiali = self.db.materiali
        self.upload_folder = "uploads"

        # Creazione della cartella per i file caricati, se non esiste
        if not os.path.exists(self.upload_folder):
            os.makedirs(self.upload_folder)

    def __del__(self):
        # Chiude la connessione al database quando l'oggetto viene distrutto
        self.client.close()

    def visualizza_materiali(self, skip=0, limit=10):
        """
        Restituisce una lista dei materiali didattici con supporto alla paginazione.
        """
        return list(self.materiali.find({}, {"_id": 0}).skip(skip).limit(limit))

    def inserisci_materiale(self, nome, descrizione, file_path):
        """
        Inserisce un nuovo materiale didattico, salvandone il file sul file system e i metadati nel database.
        """
        if not nome or not descrizione:
            raise ValueError("Nome e descrizione sono obbligatori.")
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Il file '{file_path}' non esiste.")

        file_name = os.path.basename(file_path)
        upload_path = os.path.join(self.upload_folder, file_name)

        try:
            with open(file_path, "rb") as file:
                with open(upload_path, "wb") as dest:
                    dest.write(file.read())
        except Exception as e:
            raise IOError(f"Errore durante il caricamento del file: {e}")

        nuovo_materiale = {"nome": nome, "descrizione": descrizione, "file_path": upload_path}
        self.materiali.insert_one(nuovo_materiale)

    def modifica_materiale(self, nome_corrente, nuovo_nome, nuova_descrizione):
        """
        Modifica i dati di un materiale didattico esistente.
        """
        if not nuovo_nome or not nuova_descrizione:
            raise ValueError("Il nuovo nome e la nuova descrizione sono obbligatori.")

        result = self.materiali.update_one(
            {"nome": nome_corrente},
            {"$set": {"nome": nuovo_nome, "descrizione": nuova_descrizione}}
        )
        return result.modified_count > 0

    def rimuovi_materiale(self, nome):
        """
        Rimuove un materiale didattico sia dal database che dal file system.
        """
        materiale = self.materiali.find_one({"nome": nome})
        if materiale and "file_path" in materiale:
            try:
                os.remove(materiale["file_path"])
            except FileNotFoundError:
                print(f"Attenzione: Il file '{materiale['file_path']}' non esiste.")
            except Exception as e:
                print(f"Errore durante la rimozione del file: {e}")

        result = self.materiali.delete_one({"nome": nome})
        return result.deleted_count > 0