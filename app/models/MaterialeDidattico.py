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
        """Chiude la connessione al database quando l'oggetto viene distrutto."""
        self.close_connection()

    def close_connection(self):
        """Chiude la connessione al database."""
        if self.client:
            self.client.close()
            print("Connessione al database chiusa")

    def visualizza_materiali(self, skip=0, limit=10):
        """
        Restituisce una lista dei materiali didattici con supporto alla paginazione.
        """
        return list(self.materiali.find({}, {"_id": 0}).skip(skip).limit(limit))

    def inserisci_materiale(self, id_materiale, tipo, titolo, descrizione, file_path):
        """
        Inserisce un nuovo materiale didattico, salvandone il file sul file system e i metadati nel database.
        """
        if not titolo or not descrizione:
            raise ValueError("Titolo e descrizione sono obbligatori.")
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

        nuovo_materiale = {
            "ID_MaterialeDidattico": id_materiale,
            "Tipo": tipo,
            "Titolo": titolo,
            "Descrizione": descrizione,
            "File_Path": upload_path
        }
        self.materiali.insert_one(nuovo_materiale)

    def modifica_materiale(self, id_materiale_corrente, nuovo_titolo, nuova_descrizione):
        """
        Modifica i dati di un materiale didattico esistente.
        """
        if not nuovo_titolo or not nuova_descrizione:
            raise ValueError("Il nuovo titolo e la nuova descrizione sono obbligatori.")

        result = self.materiali.update_one(
            {"ID_MaterialeDidattico": id_materiale_corrente},
            {"$set": {"Titolo": nuovo_titolo, "Descrizione": nuova_descrizione}}
        )
        return result.modified_count > 0

    def rimuovi_materiale(self, id_materiale):
        """
        Rimuove un materiale didattico sia dal database che dal file system.
        """
        materiale = self.materiali.find_one({"ID_MaterialeDidattico": id_materiale})
        if materiale and "File_Path" in materiale:
            try:
                os.remove(materiale["File_Path"])
            except FileNotFoundError:
                print(f"Attenzione: Il file '{materiale['File_Path']}' non esiste.")
            except Exception as e:
                print(f"Errore durante la rimozione del file: {e}")

        result = self.materiali.delete_one({"ID_MaterialeDidattico": id_materiale})
        return result.deleted_count > 0