from Backend.Extensiones import db
from Modelos.Modelos import Alumnos,FactoresDeRiesgo,FactoresPorAlumno,Inicio_Sesion,Inscripciones,Grupos,grupos_materias,Materias,Grupos
from flask import jsonify, Blueprint, request
from sqlalchemy.orm import joinedload
Alumnos_bp = Blueprint('alumnos',__name__)
from Funciones.Decodificar import token_required



@Alumnos_bp.route('/api/alumnos',methods=['GET'])
@token_required
def obtener_alumnos_factores(id_login):
    try:
        
        docente = Inicio_Sesion.query.filter_by(id=id_login).first()
        if not docente:
            raise ValueError("No se encontró el docente con ese ID de sesión.")
        
        rol = docente.docente.rol if docente.docente else 'DOCENTE'
        id_materia = request.args.get("id_materia", type=int)
        id_grupo = request.args.get("id_grupo", type=int)
        

        if rol == 'ADMINISTRADOR':
            alumnos = Alumnos.query.all()
            resultado = []
            for a in alumnos:
                resultado.append({
                    "numeroDeControl": a.no_control,
                    "nombre": a.nombre,
                    "apellidoPaterno": a.apellido_paterno,
                    "apellidoMaterno": a.apellido_materno,
                    "factoresDeRiesgo": [f.factor.nombre for f in a.factores_de_riesgo]
                })
            return jsonify(resultado), 200
        
        
        id_docente = docente.id_docente
        
    
        if not id_materia or not id_grupo:
            return jsonify({'ERROR': 'Se requieren id_materia e id_grupo para docentes'}), 400
        
        alumnos = (
            db.session.query(Alumnos)
            .join(Inscripciones, Inscripciones.no_control_alumno == Alumnos.no_control)
            .join(Grupos, Grupos.id == Inscripciones.id_grupo)
            .join(grupos_materias, grupos_materias.id_grupo == Grupos.id)
            .filter(
                grupos_materias.id_docente == id_docente,
                grupos_materias.id_materia == id_materia,
                grupos_materias.id_grupo == id_grupo
            )
            .all()
        )

        resultado = []
        for a in alumnos:
            resultado.append({
                "numeroDeControl": a.no_control,
                "nombre": a.nombre,
                "apellidoPaterno": a.apellido_paterno,
                "apellidoMaterno": a.apellido_materno,  # si es None, JSON lo mantiene
                "factoresDeRiesgo": [f.factor.nombre for f in a.factores_de_riesgo]
            })
        return jsonify(resultado),200
    except Exception as e:
        print(f'Error {str(e)}')
        return jsonify({'ERROR': f'Error al cargar los alumnos: {str(e)}'}), 500


@Alumnos_bp.route('/api/alumno_detalle/<no_control>', methods=['GET'])
@token_required
def obtener_alumno_detalle(no_control, id_login):
    try:
        alumno = Alumnos.query.filter_by(no_control=no_control).first()
        if not alumno:
            return jsonify({'ERROR': 'Alumno no encontrado'}), 404
        
        docente = Inicio_Sesion.query.filter_by(id=id_login).first()
        if not docente or not docente.docente:
            return jsonify({'ERROR': 'Usuario no encontrado'}), 401
        
        rol = docente.docente.rol if docente.docente else 'DOCENTE'
        id_materia = request.args.get("id_materia", type=int)

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

       
        if rol == 'DOCENTE' and not id_materia:
            return jsonify({'ERROR': 'Se requiere id_materia para docentes'}), 400

        
        for inscripcion in alumno.inscripciones:
            grupo = inscripcion.grupo

            if not grupo:
                continue

            # Recorrer las materias del grupo
            for relacion in grupo.grupos_materias:
                materia = relacion.materia

                if not materia:
                    continue
                
                
                if rol == 'DOCENTE' and materia.id != id_materia:
                    continue
                
                
                calificaciones = [
                    {
                        "unidad": cal.unidad,
                        "calificacion": cal.calificacion,
                        "faltas": cal.faltas
                    }
                    for cal in inscripcion.calificaciones
                    if cal and cal.id_materia == materia.id
                ]

                resultado['inscripciones'].append({
                    "grupo": grupo.grupo,
                    "nombreMateria": materia.nombre,
                    "serieMateria": materia.serie,
                    "calificaciones": calificaciones
                })

        return jsonify(resultado)

    except Exception as e:
        return jsonify({'ERROR': f'Error al cargar el alumno: {str(e)}'}), 500

#agragar factors

@Alumnos_bp.route('/api/alumnos/factores-riesgo')
def obtener_factores():
    try:
        factores = FactoresDeRiesgo.query.all()
        
        return jsonify([f.to_dict() for f in factores]),200
    except Exception as e:
        return jsonify({'error':f'Error al obtener los factores {str(e)}'}),500


@Alumnos_bp.route('/api/alumnos/factor-alumno', methods=['POST'])
def crear_factor_alumno():
    try:
        data = request.get_json() or request.form
        no_control = data.get('no_control','').strip()
        factores = data.get('id_factor',[])

        if not no_control:
            return jsonify({'error','Faltan datos: Numero de control'}),400
        
        if not factores:
            return jsonify({'error','No se proporcionan factores de riesgo'})
        
        if isinstance(factores, str):
            # Si llega como cadena (por ejemplo: "1,2,3"), la convertimos a lista
            factores = [f.strip() for f in factores.split(',') if f.strip().isdigit()]

        alumno = Alumnos.query.filter_by(no_control=no_control).first()
        if not alumno:
            return jsonify({'error':f'No se encontro un alumno con el numero de control {no_control}'}),404
        

        nuevos_registros = []
        for id_factor in factores:
            existente = FactoresPorAlumno.query.filter_by(
                id_factor=id_factor, no_control_alumno=no_control
            ).first()
            if not existente:
                nuevo = FactoresPorAlumno(
                    id_factor=int(id_factor),
                    no_control_alumno=no_control
                )
                nuevos_registros.append(nuevo)

        if not nuevos_registros:
            return jsonify({'warning': 'El alumno ya tenía todos los factores asignados.'}), 200
        
        db.session.add_all(nuevos_registros)
        db.session.commit()

        return jsonify({'status':'success','message':'Factor guardado con excito'}),200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error':f'Error al crear el factor alumno {str(e)}'}),500
    

@Alumnos_bp.route('/api/alumnos/materias', methods=['GET'])
def get_materias():
    try:
        materia = Materias.query.all()
        resultado = []
        for m in materia:
            resultado.append({
                'Nombre':m.nombre,
                'id':m.id
            })
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'ERROR': f'Error al cargar las materias: {str(e)}'}), 500
    

@Alumnos_bp.route('/api/alumnos/grupos', methods=['GET'])
def get_grupos():
    try:
        grupos = Grupos.query.all()
        resultado = []
        for g in grupos:
            resultado.append({
                'Nombre':g.grupo,
                'id':g.id
            })
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({'ERROR': f'Error al cargar los grupos: {str(e)}'}), 500
        