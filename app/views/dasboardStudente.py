from flask import Blueprint, request
from app.controllers.DashboardControl import DashboardController
from app.controllers.loginControl import student_required

# Crea il blueprint
dashboard_bp = Blueprint('dashboard', __name__, template_folder='../templates')

# Rotta per la dashboard
@dashboard_bp.route('/dashboard')
@student_required
def dashboardStudente():
    """
    Visualizza la dashboard per un utente specifico.
    """
    # Ottieni i parametri dalla query string
    cf_studente = request.args.get("cf_studente", "RSSMRA80A01H501Z")
    id_classe = int(request.args.get("ID_classe", 101))

    # Usa il controller per ottenere i dati
    return DashboardController.mostra_dashboard(cf_studente, id_classe)
