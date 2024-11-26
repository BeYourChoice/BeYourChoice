from app.models.ClasseVirtuale import ClasseVirtuale


class ClasseVirtualeControl:
    def __init__(self):
        self.model = ClasseVirtuale()

    def creazioneClasseVirtuale(self, NomeClasse, Descrizione):
        """
        Crea una nuova classe virtuale.
        """
        try:
            messaggio = self.model.creazioneClasseVirtuale(NomeClasse, Descrizione)
            print(messaggio)
        except ValueError as e:
            print(f"Errore: {e}")
            raise

    def inserisci_studente_classe(self, IdCasse, IdStudente):
        """
        Inserisce uno studente in una classe virtuale.
        """
        try:
            messaggio = self.model.inserimentoClasseStudente(IdCasse, IdStudente)
            print(messaggio)
        except ValueError as e:
            print(f"Errore: {e}")
            raise

    def rimozioneClasseStudente(self, IdClasse, IdStudente):
        """
        Rimuove uno studente da una classe virtuale.
        """
        try:
            messaggio = self.model.rimozioneClasseStudente(IdClasse,IdStudente)
            print(messaggio)
        except ValueError as e:
            print(f"Errore: {e}")
            raise

    def mostra_classe(self, IdClasse):
        """
        Mostra tutti gli studenti di una classe virtuale.
        """
        try:
            messaggio = self.model.mostra_classe(IdClasse)
            print(messaggio)
        except ValueError as e:
            print(f"Errore: {e}")
            raise
