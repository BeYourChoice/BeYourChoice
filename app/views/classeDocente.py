from flask import *
from app.controllers.classeVirtualeControl import ClasseVirtualeControl
from app.controllers.loginControl import teacher_required, student_required

# Crea il blueprint
classedocente = Blueprint('classedocente', __name__)
# Configura il database manager
classe_virtuale_control = ClasseVirtualeControl()


@classedocente.route('/classe/<int:id_classe>', methods=['GET', 'POST'])
@teacher_required
def classe_docente(id_classe):
    print("La route /ClasseDocente è stata chiamata!")  # Debug
    session['id_classe'] = id_classe

    try:
        # Ottieni l'ID della classe dalla query string (se non è presente, usa 101 come default)
        print(f"ID_Classe ricevuto: {id_classe}")
        dati_classe = classe_virtuale_control.mostra_studenti_classe(id_classe)
        print(f"Dati classe ricevuti: {dati_classe}")  # Aggiunto per debugging

        if "error" in dati_classe:
            return render_template("classeDocente.html")

        # Assicurati che 'dati_classe' sia un dizionario o un oggetto con l'attributo 'id_classe'
        print(dati_classe)  # Debugging
        return render_template("classeDocente.html", classe=dati_classe)

    except Exception as e:
        return render_template("errore.html", messaggio=f"Errore: {str(e)}")


@classedocente.route('/cerca-studente', methods=['GET'])
def cerca_studente():
    query = request.args.get('query', '').strip()
    id_classe = session.get('id_classe', None)  # Recupera l'ID della classe dalla sessione

    if not id_classe:
        return jsonify([])  # Nessuna classe selezionata

    if query == '':
        # Se la query è vuota, restituisci tutti gli studenti della classe
        studenti = classe_virtuale_control.mostra_studenti_classe(id_classe)
    else:
        # Altrimenti, restituisci solo gli studenti filtrati
        studenti = classe_virtuale_control.cerca_studenti_classe(query, id_classe)

    return jsonify(studenti)

@classedocente.route('/cerca-studente-istituto', methods=['GET'])
def cerca_studente_istituto():
    query = request.args.get('query', '').strip()
    id_classe = session.get('id_classe', None)  # Recupera l'ID della classe dalla sessione
    if not id_classe:
        return jsonify([])  # Nessuna classe selezionata

    if query == '':
        # Se la query è vuota, restituisci tutti gli studenti della classe
        studenti = classe_virtuale_control.mostra_studenti_istituto("Liceo scientifico galileo galilei")
    else:

        # Altrimenti, restituisci solo gli studenti filtrati
        studenti = classe_virtuale_control.cerca_studenti_istituto(query)

    return jsonify(studenti)

@classedocente.route('/classestudente/<int:id_classe>', methods=['GET', 'POST'])
@student_required
def classe_studente(id_classe):
    print("La route /ClasseStudente è stata chiamata!")  # Debug
    print(id_classe)
    if id_classe == 0:
        # Se id_classe è 0, reindirizza alla pagina noclasse
        return redirect(url_for('classedocente.no_classe'))

    try:
        dati_classe = classe_virtuale_control.mostra_studenti_classe(id_classe)
        print(f"Dati classe ricevuti: {dati_classe}")  # Debug

        if "error" in dati_classe:
            return render_template("errore.html", messaggio=dati_classe["error"])

        return render_template("classeStudente.html", classe=dati_classe)

    except Exception as e:
        return render_template("errore.html", messaggio=f"Errore: {str(e)}")


# Route per la pagina noclasse
@classedocente.route('/noclasse', methods=['GET'])
@student_required
def no_classe():
    return render_template("noClasse.html", messaggio="Nessuna classe selezionata.")

# Route per la pagina manutenzione
@classedocente.route('/manutenzione', methods=['GET'])
def manutenzione():
    return render_template("error404.html", messaggio="Manutenzione in corso.")

# Route per la pagina manutenzione
@classedocente.route('/logoaction', methods=['GET'])
def logo_action():
    return render_template("logoaction.html", messaggio="Manutenzione in corso.")

@classedocente.route('/rimuovi-studente', methods=['POST'])
@teacher_required
def rimuovi_studente_classe():
    try:
        # Ottieni l'ID dello studente dalla richiesta
        data = request.get_json()
        id_studente = data.get('id_studente')

        if not id_studente:
            return jsonify({'error': 'ID studente mancante'}), 400

        # Chiama il metodo per rimuovere lo studente
        result = classe_virtuale_control.rimuovi_studente_classe(id_studente)

        # Se il risultato è positivo, invia una risposta di successo
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@classedocente.route('/aggiungi-studente', methods=['POST'])
@teacher_required
def aggiungi_studente_classe():
    try:
        # Ottieni i dati dallo studente dalla richiesta
        data = request.get_json()  # Dati inviati come JSON
        id_studente = data.get('id_studente')
        id_classe = int(data.get('id_classe'))  # Conversione esplicita a intero

        if not id_studente or not id_classe:
            return jsonify({'error': 'ID dello studente o della classe non forniti'}), 400

        # Aggiungi lo studente alla classe
        result = classe_virtuale_control.aggiungi_studente_classe(id_studente, id_classe)

        # Se l'inserimento è avvenuto con successo
        if result:
            return jsonify({'success': True}), 200
        else:
            return jsonify({'error': 'Errore durante l\'aggiunta dello studente'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500