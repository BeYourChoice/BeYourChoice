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
                print(f"Nome: {materiale['nome']}, Descrizione: {materiale['descrizione']}, "
                      f"Percorso file: {materiale['file_path']}")
        else:
            print("Nessun materiale trovato.")

    def inserisci_materiale(self, nome, descrizione, file_path):
        """
        Inserisce un nuovo materiale.
        """
        try:
            self.model.inserisci_materiale(nome, descrizione, file_path)
            print(f"Materiale '{nome}' inserito con successo!")
        except FileNotFoundError as e:
            print(f"Errore: {e}")
        except ValueError as e:
            print(f"Errore: {e}")
        except IOError as e:
            print(f"Errore durante l'inserimento del materiale: {e}")

    def modifica_materiale(self, nome_corrente, nuovo_nome, nuova_descrizione):
        """
        Modifica i dati di un materiale esistente.
        """
        try:
            success = self.model.modifica_materiale(nome_corrente, nuovo_nome, nuova_descrizione)
            if success:
                print(f"Materiale '{nome_corrente}' modificato con successo!")
            else:
                print(f"Errore: Materiale '{nome_corrente}' non trovato o dati invariati.")
        except ValueError as e:
            print(f"Errore: {e}")

    def rimuovi_materiale(self, nome):
        """
        Rimuove un materiale esistente.
        """
        success = self.model.rimuovi_materiale(nome)
        if success:
            print(f"Materiale '{nome}' rimosso con successo!")
        else:
            print(f"Errore: Materiale '{nome}' non trovato.")