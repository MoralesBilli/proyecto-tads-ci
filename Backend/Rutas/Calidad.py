from Extensiones import db
from flask import jsonify, Blueprint
from Modelos.Modelos import Calificaciones,FactoresPorAlumno
from sqlalchemy import func

Calidad_bp = Blueprint('calidad',__name__)

@Calidad_bp.route('/api/calidad/histograma',methods=['GET'])
def obtener_datos_histograma():
    try:
        calificacion = Calificaciones.query.all()
        
        conteo ={}

        for c in calificacion:
            cal = c.calificacion
            conteo[cal] = conteo.get(cal,0) + 1
        
        resultado = [{'calificacion': cali, 'qty':qty} for cali, qty in sorted(conteo.items()) ]
        return jsonify(resultado)

    except Exception as e:
        return jsonify({'error':f'Error al obtener los datos para el histograma {str(e)}'})
    

@Calidad_bp.route('/api/calidad/pareto',methods=['GET'])
def obtener_datos_pareto():
    try:
        factor_alumno = FactoresPorAlumno.query.all()
        conteo = {}
        for f in factor_alumno:
            fac_nombre = f.factor.nombre if f.factor else "Desconocido"
            conteo[fac_nombre] = conteo.get(fac_nombre, 0) + 1

            resultado = [{'factor':nombre,'qty':qty} for nombre, qty in sorted(conteo.items())]

            return jsonify(resultado)


    except Exception as e:
        return jsonify({'error':f'Error al obtener los datos para el diagrama de pareto {str(e)}'})
  


@Calidad_bp.route('/api/calidad/dispersion',methods=['GET'])
def obtener_datos_dispersion():
    try:

        calificacion = Calificaciones.query.all()
        resultado = []
        for ca in calificacion:
            resultado.append({
                'calificacion': ca.calificacion,
                'faltas':ca.faltas
            })
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'error':f'Error al obtener los datos para el diagrama de dispersion {str(e)}'})

@Calidad_bp.route('/api/calidad/control',methods=['GET'])
def obtener_datos_control():
    try:
        resultados = (
            db.session.query(Calificaciones.Unidad,
                             func.avg(Calificaciones.calificacion).label('calificacionPromedio'),
                             func.avg(Calificaciones.faltas).label('faaltasPromedio')
                             ).group_by(Calificaciones.unidad).order_by(Calificaciones.unidad).all()
                             
        )
        respuesta= [{
            'unidad':r.unidad,
            'calificacionPromedio':round(r.calificacion_promedio, 2),
            'faltaspromedio': round(r.faltas_promedio, 2)

        } for r in resultados]

        return jsonify(respuesta)

    except Exception as e:
        return jsonify({'error':f'Error al obtener los datos para el diagrama de control {str(e)}'})
