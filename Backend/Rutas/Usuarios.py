from flask import Blueprint, request,jsonify
from Backend.Extensiones import db
from Funciones.Agregar_docente import crear_docente as crear_docente2
Usuarios_bp = Blueprint('usuarios',__name__)

import re


@Usuarios_bp.route('/api/crear-usuario',methods=['POST'])
def crear_docente():
    try:
        clave_docente = request.form.get('clave')
        nombre = request.form.get('nombre')
        apellido_paterno = request.form.get('apellidopa')
        apellido_materno = request.form.get('apellidoma')
        num_telefono = request.form.get('telefono')
        correo =  request.form.get('correo')

        patron_nombre = r'^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s]+$'
        patron_correo = r'^[a-zA-Z0-9._%+-]+@tectijuana\.edu\.mx$'

        nombres = {'Nombre':nombre,'Apellido paterno':apellido_paterno,'Apellido materno': apellido_materno}

        for etiqueta, n in nombres.items():
            if not  re.match(patron_nombre,n):
                return jsonify({'error':f'Formato de {etiqueta} incorrecto'}),400
        #validaciones
        if not re.match(patron_correo,correo):
            return jsonify({'error':'Formato de correo incorrecto'}),400
        

        
        if len(str(num_telefono)) != 10:
            return jsonify({'error':'Numero de telefono es incorrecto'}),400
        
        if not str(clave_docente).isdigit():
            return jsonify({'error':'La calve debe de ser numerica'}),400

        exito, mensaje = crear_docente2(clave_docente, nombre, apellido_paterno, apellido_materno, num_telefono, correo)
        if exito:
            
            return jsonify({'status':'success','message':mensaje}), 201
        
        else:
            return jsonify({'error':mensaje}), 400

    except Exception as e:
        db.session.rollback()
        return jsonify({'error':'Error al registrar al docente'}),500