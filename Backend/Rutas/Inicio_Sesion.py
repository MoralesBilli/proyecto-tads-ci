from flask import Blueprint, request,jsonify,current_app
from Modelos.Modelos import Inicio_Sesion
import bcrypt
import jwt
from datetime import datetime, timedelta
from Funciones.Decodificar import token_required
from Backend.Extensiones import db

Inicio_sesion_bp = Blueprint('inicio_sesion', __name__)

@Inicio_sesion_bp.route('/api/inicio_sesion', methods=['POST'])
def login():
    try:
        data = request.get_json()
        usuario = data.get('user')
        contraseña = data.get('password')

        inicio = Inicio_Sesion.query.filter_by(usuario=usuario).first()

        if not inicio:
            return jsonify({'error':'Usuario no encontrado'}),401
        
        primera_vez = inicio.primera_vez
        
        
        rol = inicio.docente.rol if inicio.docente else 'DOCENTE'

        if bcrypt.checkpw(contraseña.encode('utf-8'), inicio.contrasena.encode('utf-8')):
            token = jwt.encode({
                'id':inicio.id,
                'doce':inicio.id_docente,
                'rol': rol,
                'exp':datetime.utcnow() + timedelta(hours=8)
            }, current_app.config['SECRET_KEY'], algorithm='HS256') 
            return jsonify({
                "success": True, 
                "message": "Login exitoso", 
                "token": token, 
                'acceso':primera_vez,
                'rol': rol
            }),200
        else:
            return jsonify({"success": False, "error": "Credenciales incorrectas"}), 401
        
    except Exception as e:
        return jsonify({'error': f'Error al iniciar sesion: {str(e)}'}),500


@Inicio_sesion_bp.route('/api/cambiar-contraseña',methods=['PUT'])
@token_required
def cambiar_contrasena(id_login):

    try:
        
        data = request.get_json()

        nueva_contrasena = data.get('nueva_contrasena')
        contrasena_actual = data.get('contrasena_actual')

        if not nueva_contrasena or not contrasena_actual :
            return jsonify({'error':'La contraseña actual y nueva contraseña son requeridas'}), 400
        
        if len(nueva_contrasena) < 8:
            return jsonify({'error': 'La nueva contraseña debe tener al menos 8 caracteres'}), 400
        if not any(c.isupper() for c in nueva_contrasena):
            return jsonify({'error': 'La nueva contraseña debe tener al menos una letra mayúscula'}), 400
        if not any(c.isdigit() for c in nueva_contrasena):
            return jsonify({'error': 'La nueva contraseña debe tener al menos un número'}), 400
        

        usuario = Inicio_Sesion.query.get(id_login)
        if not usuario:
            return jsonify({'error':'Usuario no encontrado'}),401

        if not bcrypt.checkpw(contrasena_actual.encode('utf-8'), usuario.contrasena.encode('utf-8')):
            return jsonify({'error': 'La contraseña actual no es correcta'}), 400
        
        hash_nuevo = bcrypt.hashpw(nueva_contrasena.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        usuario.contrasena = hash_nuevo
        usuario.primera_vez = False  # por si quieres marcar que ya cambió
        db.session.commit()
        

        return jsonify({'mensaje': 'Contraseña actualizada exitosamente'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Error interno del servidor'}), 500
    