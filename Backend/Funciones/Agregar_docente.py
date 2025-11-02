from Modelos.Modelos import Docente,Inicio_Sesion
from Extensiones import db
import bcrypt

def crear_docente(clave_docente, nombre, apellido_paterno, apellido_materno, num_telefono, correo):
   
    try:
        # Validar campos obligatorios
        campos = [clave_docente, nombre, apellido_paterno, apellido_materno, num_telefono, correo]
        if not all(campos):
            return False, "Todos los campos son obligatorios."

        # Verificar si ya existe
        if Docente.query.filter_by(clave_docente=clave_docente).first():
            return False, f"Ya existe un docente con la clave {clave_docente}"

        # Crear docente
        nuevo_docente = Docente(
            clave_docente=clave_docente,
            nombre=nombre,
            apellido_paterno=apellido_paterno,
            apellido_materno=apellido_materno,
            num_telefono=num_telefono,
            correo=correo 
        )
        db.session.add(nuevo_docente)
        db.session.flush()  # para obtener id si es necesario

        # Crear login
        contrasena_hash = bcrypt.hashpw(clave_docente.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        nuevo_login = Inicio_Sesion(
            id_docente=clave_docente,
            usuario=clave_docente,
            contrasena=contrasena_hash,
            primera_vez=True
        )
        db.session.add(nuevo_login)

        db.session.commit()
        return True, "Docente y login registrados correctamente"

    except Exception as e:
        db.session.rollback()
        return False, f"Error al registrar al docente: {str(e)}"
