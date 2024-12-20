from flask import Blueprint, render_template, request

from app.controllers.loginControl import teacher_required
from app.controllers.scenarioControl import scenarioControl
from app.models.scenarioModel import ScenarioModel

# Crea un Blueprint per il modulo Scenario
scenario_bp = Blueprint('scenario_bp', __name__)

@scenario_bp.route('/scenarioVirtuale',methods=['GET', 'POST'])
@teacher_required
def scenario_virtuale():
    scenarioModel = ScenarioModel()
    id = scenarioModel.get_ultimo_scenario_id()
    if id is None: id = 0
    elif id == 0: id = 1
    elif id > 0: id=id+1
    titolo = request.form.get('titolo', '').strip()
    descrizione = request.form.get('descrizione', '').strip()
    modalita = request.form.get('modalita', '').strip()
    argomento = request.form.get('argomento', '').strip()
    return scenarioControl.registra_scenario(id,titolo, descrizione, modalita, argomento)

@scenario_bp.route('/postAssociazione')
@teacher_required
def postAssociazione():
    return render_template("scenarioVirtuale.html")

