from Modelos.Modelos import Auditrail
from flask import Blueprint, request,jsonify

Logs_bp = Blueprint('logs',__name__)

@Logs_bp.route('/api/logs', methods=['GET'])
def obtener_logs():
    try:
        logs = Auditrail.query.all()
        if not logs:  
            return jsonify({'mensaje': 'No hay registros de logs disponibles.'}), 200
        
        return jsonify([log.to_dict() for log in logs]),200
    except Exception as e:
        return jsonify({'error':f'Error al obtener los logs {str(e)}'}),500