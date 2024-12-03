import logging

import bcrypt
from flask import flash, jsonify, session, url_for, redirect
from werkzeug.security import generate_password_hash, check_password_hash

from databaseManager import DatabaseManager


class ProfiloControl:
    def __init__(self, db_manager):
        self.db_manager = DatabaseManager()

    def get_profilo_studente(self, email):
        try:
            studente_collection = self.db_manager.get_collection("Studente")
            query = {"email": email}
            profilo_studente = list(studente_collection.find(query))
            return profilo_studente
        except Exception as e:
            logging.error(f"Errore nel recuperare il profilo dello studente dall'email {email}: {str(e)}")
            return []

    def get_profilo_docente(self, email):
        try:
            docente_collection = self.db_manager.get_collection("Docente")
            query = {"email": email}
            profilo_docente = list(docente_collection.find(query))
            return profilo_docente
        except Exception as e:
            logging.error(f"Errore nel recuperare il profilo del docente dall'email {email}: {str(e)}")
            return []

    def update_profilo_studente(self, email, nuovi_dati):
        try:
            result = self.studente_collection.update_one({"email": email}, {"$set": nuovi_dati})
            return result.modified_count > 0
        except Exception as e:
            logging.error(f"Errore nell'aggiornare il profilo dello studente per l'email {email}: {str(e)}")
            return False

    def update_profilo_docente(self, email, nuovi_dati):
        try:
            result = self.docente_collection.update_one({"email": email}, {"$set": nuovi_dati})
            return result.modified_count > 0
        except Exception as e:
            logging.error(f"Errore nell'aggiornare il profilo del docente per l'email {email}: {str(e)}")
            return False

    def cambia_password(self, vecchia_password, nuova_password):
        """
        Cambia la password di un docente utilizzando l'email dalla sessione.
        """
        docente_collection = self.db_manager.get_collection("Docente")

        # Ottieni l'email dalla sessione
        email = session.get("email")

        if not email:
            return "Errore: Nessuna email trovata nella sessione. Effettua il login."

        # Trova il docente nel database tramite l'email
        docente = docente_collection.find_one({"email": email})

        if not docente:
            return "Errore: Docente non trovato."

        # Verifica la vecchia password
        if not bcrypt.checkpw(vecchia_password.encode('utf-8'), docente['password']):
            return "Errore: Vecchia password errata."

        # Cifra la nuova password
        nuova_password_hash = bcrypt.hashpw(nuova_password.encode('utf-8'), bcrypt.gensalt())

        # Aggiorna la password nel database
        result = docente_collection.update_one(
            {"email": email},
            {"$set": {"password": nuova_password_hash}}
        )

        if result.modified_count > 0:
            if result.modified_count > 0:
                flash("Password aggiornata con successo!", "message_profile")
            else:
                flash("Errore: Password non aggiornata.", "message_profile")

            return redirect(url_for('profilo.gestione_profilo'))