from flask import Blueprint, render_template, request

from app.controllers.scenarioControl import scenarioControl

# Crea un Blueprint per il modulo Scenario
scenario_bp = Blueprint('scenario_bp', __name__)

@scenario_bp.route('/scenarioVirtuale',methods=['GET', 'POST'])
def scenario_virtuale():
    titolo = request.form.get('titolo', '').strip()
    descrizione = request.form.get('descrizione', '').strip()
    modalita = request.form.get('modalita', '').strip()
    argomento = request.form.get('argomento', '').strip()
    return scenarioControl.registra_scenario(titolo, descrizione, modalita, argomento)
