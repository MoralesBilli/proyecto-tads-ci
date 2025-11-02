from flask import request, jsonify
import jwt
import os
import inspect


SECRET_KEY = os.getenv('SECRET_KEY')

def token_required(f):
    def decorator(*args, **kwargs):
        
        token = None
        if 'Authorization' in request.headers:
        
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]
        if not token:
            
            return jsonify({'message': 'Token es requerido'}), 401
        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            id_login = data.get('id')
          
            
            
        except Exception as e:
            return jsonify({'message': 'Token inválido o expirado'}), 401
        
        params = inspect.signature(f).parameters
        if 'id_login' in params:
            return f(id_login=id_login, *args, **kwargs)
        else:
            return f(*args, **kwargs)

    
    decorator.__name__ = f.__name__
    return decorator