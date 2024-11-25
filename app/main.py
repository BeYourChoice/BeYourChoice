# main.py
from app.controllers.MaterialeControl import MaterialeControl

def main():
    controllo_materiale = MaterialeControl()

    # Esempio di inserimento
    controllo_materiale.inserisci_materiale(
        id_materiale=2001,
        tipo="Documento",
        titolo="Introduzione alla Costituzione",
        descrizione="Testo esplicativo sui primi 12 articoli della Costituzione Italiana",
        file_path="app/uploads/Introduzione_Costituzione.txt"
    )

    # Esempio di visualizzazione
    controllo_materiale.visualizza_materiali()

    # Esempio di modifica
    controllo_materiale.modifica_materiale(
        id_materiale_corrente=2001,
        nuovo_titolo="Introduzione alla Costituzione - Parte 2",
        nuova_descrizione="Nuovo video esplicativo sui successivi articoli della Costituzione Italiana"
    )

    # Esempio di rimozione
    controllo_materiale.rimuovi_materiale(id_materiale=2001)

if __name__ == "__main__":
    main()
