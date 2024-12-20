from token import STRING

from flask import Blueprint, request, render_template, session
from app.controllers.classeVirtualeControl import ClasseVirtualeControl
from app.controllers.loginControl import teacher_required

# Crea il blueprint
inserimentostudente = Blueprint('inserimentostudente', __name__, template_folder='../templates')
# Configura il database manager
classe_virtuale_control = ClasseVirtualeControl()


@inserimentostudente.route('/', methods=['GET', 'POST'])
@teacher_required
def inserimento_studente():
    print("La route /InserimentoStudente stata chiamata!")  # Debug
    try:
        # Ottieni l'ID della classe dalla query string (se non è presente, usa 101 come default)
        scuola_appartenenza = session.get('sda')
        print(f"Sda ricevuto: {scuola_appartenenza}")  # Aggiunto per debugging

        # Usa il controller per ottenere i dati degli studentiErrore nell'aggiunta dello studente alla classe.
        dati_classe = classe_virtuale_control.mostra_studenti_istituto(scuola_appartenenza)
        print(f"Dati classe ricevuti: {dati_classe}")  # Aggiunto per debugging
        if "error" in dati_classe:
            return render_template("errore.html", messaggio=dati_classe["inserimentoStudente.html"])

            # Passa i dati al template classeDocente.html
        return render_template("inserimentoStudente.html", classe=dati_classe)

    except Exception as e:
        return render_template("inserimentoStudente.html", messaggio=f"Errore: {str(e)}")
