from flask import Blueprint, request,jsonify
from Extensiones import db
from Funciones.Agregar_docente import crear_docente as crear_docente2
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

        exito, mensaje = crear_docente2(clave_docente, nombre, apellido_paterno, apellido_materno, num_telefono, correo)
        if exito:
            return jsonify({'status':'success','message':mensaje}), 201
        else:
            return jsonify({'error':mensaje}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error':'Error al registrar al docente'})