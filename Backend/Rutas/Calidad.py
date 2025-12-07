from Backend.Extensiones import db
from flask import jsonify, Blueprint, request
from Modelos.Modelos import Calificaciones,FactoresPorAlumno,Inicio_Sesion,Inscripciones,Alumnos
from sqlalchemy import func
from Funciones.Decodificar import token_required

Calidad_bp = Blueprint('calidad',__name__)

@Calidad_bp.route('/api/calidad/histograma',methods=['GET'])
@token_required
def obtener_datos_histograma(id_login):
    try:
        
        inicio = Inicio_Sesion.query.filter_by(id=id_login).first()
        if not inicio or not inicio.docente:
            return jsonify({'error': 'Usuario no encontrado'}), 401
        
        rol = inicio.docente.rol
        id_materia = request.args.get("id_materia", type=int)
        
       
        if rol == 'ADMINISTRADOR':
            calificacion = Calificaciones.query.all()
        else:
           
            if not id_materia:
                return jsonify({'error': 'Se requiere id_materia para docentes'}), 400
            calificacion = Calificaciones.query.filter_by(id_materia=id_materia).all()
        
        conteo ={}

        for c in calificacion:
            cal = c.calificacion
            conteo[cal] = conteo.get(cal,0) + 1
        
        resultado = [{'calificacion': cali, 'qty':qty} for cali, qty in sorted(conteo.items()) ]
        return jsonify(resultado)

    except Exception as e:
        return jsonify({'error':f'Error al obtener los datos para el histograma {str(e)}'}), 500
    

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
        return jsonify({'error':f'Error al obtener los datos para el diagrama de pareto {str(e)}'}), 500
  


@Calidad_bp.route('/api/calidad/dispersion',methods=['GET'])
@token_required
def obtener_datos_dispersion(id_login):
    try:
        inicio = Inicio_Sesion.query.filter_by(id=id_login).first()
        if not inicio or not inicio.docente:
            return jsonify({'error': 'Usuario no encontrado'}), 401
        
        rol = inicio.docente.rol
        id_materia = request.args.get("id_materia", type=int)
        
        if rol == 'ADMINISTRADOR':
            calificacion = Calificaciones.query.all()
        else:
            if not id_materia:
                return jsonify({'error': 'Se requiere id_materia para docentes'}), 400
            calificacion = Calificaciones.query.filter_by(id_materia=id_materia).all()
        
        resultado = []
        for ca in calificacion:
            resultado.append({
                'calificacion': ca.calificacion,
                'faltas':ca.faltas
            })
        return jsonify(resultado)
    
    except Exception as e:
        return jsonify({'error':f'Error al obtener los datos para el diagrama de dispersion {str(e)}'}), 500

@Calidad_bp.route('/api/calidad/control',methods=['GET'])
@token_required
def obtener_datos_control(id_login):
    try:
        inicio = Inicio_Sesion.query.filter_by(id=id_login).first()
        if not inicio or not inicio.docente:
            return jsonify({'error': 'Usuario no encontrado'}), 401
        
        rol = inicio.docente.rol
        id_materia = request.args.get("id_materia", type=int)
        
        query = db.session.query(
            Calificaciones.unidad,
            func.avg(Calificaciones.calificacion).label('calificacion_promedio'),
            func.avg(Calificaciones.faltas).label('faltas_promedio')
        )
        
        if rol != 'ADMINISTRADOR':
            if not id_materia:
                return jsonify({'error': 'Se requiere id_materia para docentes'}), 400
            query = query.filter(Calificaciones.id_materia == id_materia)
        
        resultados = query.group_by(Calificaciones.unidad).order_by(Calificaciones.unidad).all()
        
        respuesta= [{
            'unidad':r.unidad,
            'calificacionPromedio':float(round(r.calificacion_promedio, 2)),
            'faltasPromedio': float(round(r.faltas_promedio, 2))

        } for r in resultados]

        return jsonify(respuesta)

    except Exception as e:
        return jsonify({'error':f'Error al obtener los datos para el diagrama de control {str(e)}'}), 500
