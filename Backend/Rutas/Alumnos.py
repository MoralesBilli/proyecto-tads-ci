from Extensiones import db
from Modelos.Modelos import Alumnos, FactoresDeRiesgo, FactoresPorAlumno
from flask import jsonify, Blueprint, request
from sqlalchemy.exc import SQLAlchemyError

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
    

@Alumnos_bp.route('/api/alumnos', methods=['POST'])
def crear_alumno():
    """
    Crea un nuevo alumno en la base de datos.
    Espera un JSON con los datos del alumno.
    """
    json_data = request.get_json()
    if not json_data:
        return jsonify({'ERROR': 'No se recibieron datos en la solicitud.'}), 400

    # --- Validación de campos obligatorios ---
    campos_obligatorios = ['no_control', 'nombre', 'apellido_paterno', 'genero', 'estado', 'semestre', 'id_carrera']
    for campo in campos_obligatorios:
        if campo not in json_data:
            return jsonify({'ERROR': f'El campo "{campo}" es obligatorio.'}), 400

    # --- Comprobar si el alumno ya existe ---
    if Alumnos.query.get(json_data['no_control']):
        return jsonify({'ERROR': f'El alumno con número de control {json_data["no_control"]} ya existe.'}), 409

    try:
        # --- Creación del nuevo alumno ---
        nuevo_alumno = Alumnos(
            no_control=json_data['no_control'],
            nombre=json_data['nombre'],
            apellido_paterno=json_data['apellido_paterno'],
            apellido_materno=json_data.get('apellido_materno'),  # Opcional
            genero=json_data['genero'],
            estado=json_data['estado'],
            semestre=json_data['semestre'],
            id_carrera=json_data['id_carrera']
        )

        db.session.add(nuevo_alumno)
        db.session.commit()

        # --- Respuesta exitosa ---
        return jsonify(nuevo_alumno.to_dict()), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        # --- Manejo de errores específicos de la base de datos ---
        error_msg = str(e.__dict__.get('orig', 'Error de base de datos'))
        if "violates foreign key constraint" in error_msg:
            return jsonify({'ERROR': 'La carrera especificada (id_carrera) no existe.'}), 400
        if "invalid input value for enum" in error_msg:
            return jsonify({'ERROR': 'Valor no válido para "genero" o "estado".'}), 400
            
        return jsonify({'ERROR': f'Error al guardar en la base de datos: {error_msg}'}), 500
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'ERROR': f'Ocurrió un error inesperado: {str(e)}'}), 500


#Endpoint para obtener un usuario en base a su numero de control 
@Alumnos_bp.route('/api/alumno_detalle/<no_control>', methods=['GET'])
def obtener_alumno_detalle(no_control):
    try:
        alumno = Alumnos.query.filter_by(no_control=no_control).first()
        if not alumno:
            return jsonify({'ERROR': 'Alumno no encontrado'}), 404

        resultado = {
            "numeroDeControl": alumno.no_control,
            "nombre": alumno.nombre,
            "apellidoPaterno": alumno.apellido_paterno,
            "apellidoMaterno": alumno.apellido_materno,
            "genero": alumno.genero,
            "estado": alumno.estado,
            "semestre": alumno.semestre,
            "nombreCarrera": alumno.carrera.nombre if alumno.carrera else None,
            "modalidadCarrera": alumno.carrera.modalidad if alumno.carrera else None,
            "factoresDeRiesgo": [f.factor.nombre for f in alumno.factores_de_riesgo],
            "inscripciones": []
        }

        # Recorrer inscripciones
        for inscripcion in alumno.inscripciones:
            grupo = inscripcion.grupo
            materia = grupo.materia if grupo else None

            ins = {
                "grupo": grupo.grupo if grupo else None,
                "nombreMateria": materia.nombre if materia else None,
                "serieMateria": materia.serie if materia else None,
                "calificaciones": []
            }

            # Calificaciones de esa inscripción
            for cal in inscripcion.calificaciones:
                ins['calificaciones'].append({
                    "unidad": cal.unidad,
                    "calificacion": cal.calificacion,
                    "faltas": cal.faltas
                })

            resultado['inscripciones'].append(ins)

        return jsonify(resultado)

    except Exception as e:
        return jsonify({'ERROR': f'Error al cargar el alumno: {str(e)}'}), 500


"""
  una petición POST a /api/alumnos/21212056/factores con el siguiente JSON en el cuerpo:

   1 {
   2   "factores_de_riesgo": [1, 3]
   3 }
"""

@Alumnos_bp.route('/api/alumnos/<no_control>/factores', methods=['POST'])
def asignar_factores_riesgo(no_control):
    """
    Asigna factores de riesgo a un alumno existente.
    """
    json_data = request.get_json()
    if not json_data or 'factores_de_riesgo' not in json_data:
        return jsonify({'ERROR': 'Se requiere una lista de factores de riesgo.'}), 400

    alumno = Alumnos.query.get(no_control)
    if not alumno:
        return jsonify({'ERROR': 'El alumno no existe.'}), 404

    try:
        # Limpiar factores de riesgo existentes
        FactoresPorAlumno.query.filter_by(no_control_alumno=no_control).delete()

        # Asignar nuevos factores
        for id_factor in json_data['factores_de_riesgo']:
            factor = FactoresDeRiesgo.query.get(id_factor)
            if factor:
                nuevo_link = FactoresPorAlumno(
                    no_control_alumno=no_control,
                    id_factor=id_factor
                )
                db.session.add(nuevo_link)

        db.session.commit()
        return jsonify(alumno.to_dict()), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'ERROR': f'Error al asignar factores: {str(e)}'}), 500
