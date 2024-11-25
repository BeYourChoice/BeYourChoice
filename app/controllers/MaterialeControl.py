from app.models.MaterialeDidattico import MaterialeDidattico

class MaterialeControl:
    def __init__(self):
        self.model = MaterialeDidattico()

    def visualizza_materiali(self, skip=0, limit=10):
        """
        Mostra i materiali con supporto alla paginazione.
        """
        materiali = self.model.visualizza_materiali(skip, limit)
        if materiali:
            for materiale in materiali:
                print(f"ID: {materiale['ID_MaterialeDidattico']}, Tipo: {materiale['Tipo']}, "
                      f"Titolo: {materiale['Titolo']}, Descrizione: {materiale['Descrizione']}, "
                      f"Percorso file: {materiale['File_Path']}")
        else:
            print("Nessun materiale trovato.")

    def inserisci_materiale(self, id_materiale, tipo, titolo, descrizione, file_path):
        """
        Inserisce un nuovo materiale.
        """
        try:
            self.model.inserisci_materiale(id_materiale, tipo, titolo, descrizione, file_path)
            print(f"Materiale '{titolo}' inserito con successo!")
        except FileNotFoundError as e:
            print(f"Errore: {e}")
        except ValueError as e:
            print(f"Errore: {e}")
        except IOError as e:
            print(f"Errore durante l'inserimento del materiale: {e}")

    def modifica_materiale(self, id_materiale_corrente, nuovo_titolo, nuova_descrizione):
        """
        Modifica i dati di un materiale esistente.
        """
        try:
            success = self.model.modifica_materiale(id_materiale_corrente, nuovo_titolo, nuova_descrizione)
            if success:
                print(f"Materiale con ID '{id_materiale_corrente}' modificato con successo!")
            else:
                print(f"Errore: Materiale con ID '{id_materiale_corrente}' non trovato o dati invariati.")
        except ValueError as e:
            print(f"Errore: {e}")

    def rimuovi_materiale(self, id_materiale):
        """
        Rimuove un materiale esistente.
        """
        success = self.model.rimuovi_materiale(id_materiale)
        if success:
            print(f"Materiale con ID '{id_materiale}' rimosso con successo!")
        else:
            print(f"Errore: Materiale con ID '{id_materiale}' non trovato.")