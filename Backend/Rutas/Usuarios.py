from Modelos.Modelos import Docente, Inicio_Sesion
from flask import Blueprint, request,jsonify
import bcrypt
from Extensiones import db

Usuarios_bp = Blueprint('usuarios',__name__)

@Usuarios_bp.route('/api/crear-usuario',methods=['POST'])
def crear_docente():
    try:
        clave_docente = request.form.get('clave')
        nombre = request.form.get('nombre')
        apellido_paterno = request.form.get('apellidopa')
        apellido_materno = request.form.get('apellidoma')
        num_telefono = request.form.get('telefono')
        correo =  request.form.get('correo')

        campos_requeridos = ['nombre','apellidopa','apellidoma','telefono','correo','clave']
        for camp in campos_requeridos:
            if not request.form.get(camp):
                return jsonify({'error':f'El campo "{camp}" es requerido. '}), 400

        docente_existente = Docente.query.filter_by(clave_docente = clave_docente).first()
        if docente_existente:
            return jsonify({'error':f'Ya existe un docente con la clave {clave_docente} registrado'}),400


        nuevo_docente =  Docente(
            nombre = nombre,
            apellido_paterno = apellido_paterno,
            apellido_materno = apellido_materno,
            num_telefono = num_telefono,
            correo = correo
        )
        db.session.add(nuevo_docente)
        db.session.flush()
        

        contrasena_hash = bcrypt.hashpw(clave_docente.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        nuevo_login = Inicio_Sesion (
            id_docente = clave_docente,
            usuario = clave_docente,
            contrasena = contrasena_hash
        )
        db.session.add(nuevo_login)
        db.session.commit()

        return jsonify({'status': 'success', 'message':'Usuario registrado'}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error':'Error al registrar al docente'})