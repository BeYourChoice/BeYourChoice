from databaseManager import DatabaseManager

class Docente:
    def __init__(self):
        self.db_manager = DatabaseManager()

    def get_classi_docente(self, id_docente):
        """
        Recupera le classi associate a un docente.
        :param cf_docente: Codice fiscale del docente.
        :return: Lista delle classi con ID_Classe e Nome_Classe.
        """
        try:
            collection = self.db_manager.get_collection("ClasseVirtuale")

            # Recupera le classi associate al docente
            classi = list(
                collection.find(
                    {"ID_Docente": id_docente},
                    {"_id": 0, "ID_Classe": 1, "Nome_Classe": 1}
                )
            )

            return classi
        except Exception as e:
            print(f"Errore nel recupero delle classi del docente: {e}")
            return []

    def close_connection(self):
        self.db_manager.close_connection()

    def get_classifica_classe(self, id_classe):
        """
        Recupera la classifica della classe con i punteggi totali di quiz e scenari.
        :param id_classe: ID della classe.
        :return: Lista degli studenti con Nome, Cognome, CF e Punteggio Totale.
        """
        try:
            studente_collection = self.db_manager.get_collection("Studente")
            studenti = list(
                studente_collection.find(
                    {"ID_Classe": id_classe},
                    {"_id": 0, "CF": 1, "Nome": 1, "Cognome": 1}
                )
            )

            # Debug: stampa gli studenti recuperati
            print("Studenti nella classe:", studenti)

            # Mappa per i punteggi
            punteggi_totali = {}

            # Calcola i punteggi dagli scenari
            scenario_collection = self.db_manager.get_collection("PunteggioScenario")
            scenari_punteggi = scenario_collection.aggregate([
                {"$group": {"_id": "$CF_Studente", "PunteggioScenari": {"$sum": "$Punteggio_Scenario"}}}
            ])

            for item in scenari_punteggi:
                punteggi_totali[item["_id"]] = {"PunteggioScenari": item["PunteggioScenari"], "PunteggioQuiz": 0}

            # Calcola i punteggi dai quiz
            quiz_collection = self.db_manager.get_collection("RisultatoQuiz")
            quiz_punteggi = quiz_collection.aggregate([
                {"$group": {"_id": "$CF_Studente", "PunteggioQuiz": {"$sum": "$Punteggio_Quiz"}}}
            ])

            for item in quiz_punteggi:
                if item["_id"] in punteggi_totali:
                    punteggi_totali[item["_id"]]["PunteggioQuiz"] = item["PunteggioQuiz"]
                else:
                    punteggi_totali[item["_id"]] = {"PunteggioScenari": 0, "PunteggioQuiz": item["PunteggioQuiz"]}

            # Debug: stampa i punteggi totali calcolati
            print("Punteggi Totali:", punteggi_totali)

            # Combina i dati degli studenti con i punteggi
            classifica = []
            for studente in studenti:
                cf_studente = studente["CF"]
                punteggio_scenari = punteggi_totali.get(cf_studente, {}).get("PunteggioScenari", 0)
                punteggio_quiz = punteggi_totali.get(cf_studente, {}).get("PunteggioQuiz", 0)
                punteggio_totale = punteggio_scenari + punteggio_quiz

                classifica.append({
                    "CF": cf_studente,
                    "Nome": studente["Nome"],
                    "Cognome": studente["Cognome"],
                    "PunteggioTotale": punteggio_totale
                })

            # Ordina la classifica per punteggio totale decrescente
            classifica.sort(key=lambda x: x["PunteggioTotale"], reverse=True)

            return classifica
        except Exception as e:
            print(f"Errore nel recupero della classifica: {e}")
            return []

    def get_storico(self, cf_studente):
        """
        Recupera lo storico dettagliato di tutte le attività svolte dallo studente.
        :param cf_studente: Codice fiscale dello studente.
        :return: Un dizionario con i dettagli dei quiz e degli scenari svolti.
        """
        try:
            # Recupero dati dal database
            risultato_quiz_collection = self.db_manager.get_collection("RisultatoQuiz")
            risultato_scenario_collection = self.db_manager.get_collection("PunteggioScenario")
            quiz_collection = self.db_manager.get_collection("Quiz")
            scenario_collection = self.db_manager.get_collection("ScenarioVirtuale")

            # Recupera i risultati dei quiz
            quiz_risultati = list(
                risultato_quiz_collection.find(
                    {"CF_Studente": cf_studente},
                    {"_id": 0, "ID_Quiz": 1, "Punteggio_Quiz": 1}
                )
            )

            # Recupera i dettagli dei quiz
            quiz_storico = []
            for risultato in quiz_risultati:
                quiz = quiz_collection.find_one(
                    {"ID_Quiz": risultato["ID_Quiz"]},
                    {"_id": 0, "Argomento": 1, "Modalità_Quiz": 1, "N_Domande": 1, "Durata": 1}
                )
                if quiz:
                    quiz["Punteggio"] = risultato["Punteggio_Quiz"]
                    quiz_storico.append(quiz)

            # Recupera i risultati degli scenari
            scenario_risultati = list(
                risultato_scenario_collection.find(
                    {"CF_Studente": cf_studente},
                    {"_id": 0, "ID_Scenario": 1, "Punteggio_Scenario": 1}
                )
            )

            # Recupera i dettagli degli scenari
            scenario_storico = []
            for risultato in scenario_risultati:
                scenario = scenario_collection.find_one(
                    {"ID_Scenario": risultato["ID_Scenario"]},
                    {"_id": 0, "Titolo": 1, "Descrizione": 1, "Argomento": 1, "Modalità": 1}
                )
                if scenario:
                    scenario["Punteggio"] = risultato["Punteggio_Scenario"]
                    scenario_storico.append(scenario)

            return {
                "Quiz": quiz_storico,
                "Scenari": scenario_storico
            }
        except Exception as e:
            print(f"Errore nel recupero dello storico: {e}")
            return {"Quiz": [], "Scenari": []}
