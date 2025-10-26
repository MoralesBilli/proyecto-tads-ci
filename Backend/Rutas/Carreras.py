from Extensiones import db
from Modelos.Modelos import Alumnos,FactoresDeRiesgo,FactoresPorAlumno
from flask import jsonify, Blueprint

Alumnos_bp = Blueprint('alumnos',__name__)

@Alumnos_bp.route('/api/alumnos',methods=['GET'])
def obtener_alumnos_factores():
    try:
        # Traer todos los alumnos
        alumnos = Alumnos.query.all()

        resultado = []
        for a in alumnos:
            resultado.append({
                "numeroDeControl": a.no_control,
                "nombre": a.nombre,
                "apellidoPaterno": a.apellido_paterno,
                "apellidoMaterno": a.apellido_materno,  # si es None, JSON lo mantiene
                "factoresDeRiesgo": [f.factor.nombre for f in a.factores_de_riesgo]
            })
        return jsonify(resultado)
    except Exception as e:
        return jsonify({'ERROR': f'Error al cargar los alumnos: {str(e)}'}), 500
