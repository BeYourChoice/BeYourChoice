from databaseManager import DatabaseManager  # Importa la classe DatabaseManager

class ScenarioModel:
    def __init__(self):
        # Utilizza la connessione esistente al database
        self.db_manager = DatabaseManager()

    def aggiungi_scenario(self, scenario_dict):
        scenario_collection = self.db_manager.get_collection("ScenarioVirtuale")
        scenario_collection.insert_one(scenario_dict)
        print("Scenario aggiunto con successo!")

    def get_last_scenario_id(self):
        # Get the collection of scenarios
        scenario_collection = self.db_manager.get_collection("ScenarioVirtuale")

        # Query the collection to get the last inserted document, sorted by _id in descending order
        last_scenario = scenario_collection.find_one(sort=[('ID_Scenario', -1)])  # -1 for descending order

        # If a scenario exists, return its ID; otherwise, return None
        if last_scenario:
            return int(last_scenario['ID_Scenario'])
        else:
            return None  # No scenarios found
