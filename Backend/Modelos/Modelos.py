from Extensiones import db

# --- Definición de Tipos ENUM ---
modalidad_enum = db.Enum('PRESENCIAL', 'SEMIPRESENCIAL', name='modalidad')
genero_enum = db.Enum('HOMBRE', 'MUJER', name='genero')
estado_alumno_enum = db.Enum('VIGENTE', 'EGRESADO', 'BAJA_TEMPORAL', 'BAJA_DEFINITIVA', name='estado_alumno')
semestre = db.Enum('1','2','3','4','5','6','7','8','9','10','11','12', name='semestres')

# --- Modelo Carreras ---

class Carreras(db.Model):
    __tablename__='carreras'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(64), nullable=False)
    modalidad = db.Column(modalidad_enum, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'modalidad': self.modalidad
        }
    
# --- Modelo Alumnos ---

class Alumnos(db.Model):
    __tablename__='alumnos'
    no_control = db.Column(db.String(16), primary_key=True, nullable=False)
    nombre = db.Column(db.String(64), nullable=False)
    apellido_paterno = db.Column(db.String(64), nullable=False)
    apellido_materno = db.Column(db.String(64))
    genero = db.Column(genero_enum, nullable=False) 
    estado = db.Column(estado_alumno_enum, nullable=False)
    semestre = db.Column(semestre, nullable=False)
    
    id_carrera = db.Column(db.Integer, db.ForeignKey('carreras.id'), nullable=False)

    # Vínculo bidireccional 
    # (alumno.carrera) y (carrera.alumnos)
    carrera = db.relationship('Carreras', backref='alumnos')
    

    def to_dict(self):
        return {
            'numeroDeControl': self.no_control,
            'nombre': self.nombre,
            'apellidoPaterno': self.apellido_paterno,
            'apellidoMaterno': self.apellido_materno,
            'genero': self.genero,
            'estado': self.estado,
            'semestre': self.semestre,
            'id_carrera': self.id_carrera,
            
            # nombre de carrera
            'nombre_carrera': self.carrera.nombre if self.carrera else None ,
            'factores_de_riesgo': [{'id_factor':factor.id, 'nombre':factor.nombre}for factor in self.factores_de_riesgo]
            
        }

class Materias(db.Model):
    __tablename__ = 'materias'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(64), nullable=False)
    serie = db.Column(db.String(64), nullable=False)
    unidades = db.Column(db.Integer, nullable=False)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nombre': self.nombre,
            'serie': self.serie,
            'unidades': self.unidades,
        }

# --- Modelo de Factores de Riesgo ---

class FactoresDeRiesgo(db.Model):
    __tablename__ = 'factores_de_riesgo'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    nombre = db.Column(db.String(64), nullable=False)
    
    def to_dict(self):
        return{
            'id': self.id,
            'nombre':self.nombre
        }
        
# --- Modelo de Factores por alumno ---

class FactoresPorAlumno(db.Model):
    __tablename__ = 'factores_por_alumno'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    id_factor = db.Column(db.Integer, db.ForeignKey('factores_de_riesgo.id'), nullable=False)
    no_control_alumno = db.Column(db.String(16), db.ForeignKey('alumnos.no_control'), nullable=False)

    # Relaciones para navegación
    factor = db.relationship('FactoresDeRiesgo', backref='alumnos_con_factor')
    alumno = db.relationship('Alumnos', backref='factores_de_riesgo')
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_factor': self.id_factor,
            'no_control_alumno':self.no_control_alumno,
            
            'nombre_factor': self.factor.nombre if self.factor else None,
            'nombre_alumno': self.alumno.nombre if self.alumno else None
        }

# --- Modelos de Inscripción y Calificaciones ---

class Grupos(db.Model):
    __tablename__ = 'grupos'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    grupo = db.Column(db.String(16))
    id_materia = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)

    materia = db.relationship('Materias', backref='grupos')
    
    def to_dict(self):
        return {
            'id': self.id,
            'grupo': self.grupo,
            'id_materia': self.id_materia,
            
            'nombre_materia': self.materia.nombre if self.materia else None
        }

class Inscripciones(db.Model):
    __tablename__ = 'inscripciones'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    
    id_grupo = db.Column(db.Integer, db.ForeignKey('grupos.id'), nullable=False)
    no_control_alumno = db.Column(db.String(16), db.ForeignKey('alumnos.no_control'), nullable=False)
    
    # Relaciones
    grupo = db.relationship('Grupos', backref='inscripciones')
    alumno = db.relationship('Alumnos', backref='inscripciones')
    

    def to_dict(self):
        return {
            'id': self.id,
            'periodo': self.periodo,
            'id_grupo': self.id_grupo,
            'no_control_alumno': self.no_control_alumno,
            
            'nombre_alumno': self.alumno.nombre if self.alumno else None,
            'info_grupo': self.grupo.grupo if self.grupo else None
        }


class Calificaciones(db.Model):
    __tablename__ = 'calificaciones'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    unidad = db.Column(db.Integer, nullable=False)
    calificacion = db.Column(db.Integer, nullable=False)
    faltas = db.Column(db.Integer, nullable=False)
    id_inscripcion = db.Column(db.Integer, db.ForeignKey('inscripciones.id'), nullable=False)
    id_materia = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    # Relación
    inscripcion = db.relationship('Inscripciones', backref='calificaciones')
    materia =db.relationship('Materias', backref='calificaciones')
    
    # --- AÑADIDO ---
    # Método 'to_dict' faltante
    def to_dict(self):
        return {
            'id': self.id,
            'unidad': self.unidad,
            'calificacion': self.calificacion,
            'faltas': self.faltas,
            'id_inscripcion': self.id_inscripcion
        }

class MateriasPorCarrera(db.Model):
    __tablename__ = 'materias_por_carrera'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    id_materia = db.Column(db.Integer, db.ForeignKey('materias.id'), nullable=False)
    id_carrera = db.Column(db.Integer, db.ForeignKey('carreras.id'), nullable=False)

    # Relaciones para navegación
    materia = db.relationship('Materias', backref='carreras_asociadas')
    carrera = db.relationship('Carreras', backref='materias_asociadas')
    
    def to_dict(self):
        return {
            'id': self.id,
            'id_materia': self.id_materia,
            'id_carrera': self.id_carrera,
            'nombre_materia': self.materia.nombre if self.materia else None,
            'nombre_carrera': self.carrera.nombre if self.carrera else None
        }
    
class Auditrail(db.Model):
        __tablename__='audit_trail'
        id = db.Column(db.Integer, primary_key=True, nullable=False)
        origin = db.Column(db.Text, nullable=False)
        accion = db.Column(db.Text,nullable=False)
        clave_docente = db.Column(db.Integer, nullable = False)
        created_at = db.Column(db.Date, nullable=False)

        def to_dict(self):
            return {
                'id':self.id,
                'accion':self.accion,
                'clave_docente':self.clave_docente,
                'create_at':self.created_at,
                'origin':self.origin
            }


class Docente(db.Model):
    __tablename__='docente'
    clave_docente = db.Column(db.Integer, primary_key = True, nullable=False)
    nombre = db.Column(db.String(64), nullable=False)
    apellido_paterno = db.Column(db.String(64), nullable=False)
    apellido_materno = db.Column(db.String(64), nullable=False)
    num_telefono = db.Column(db.String(18), nullable=False)
    correo = db.Column(db.Text, nullable = False)

    def to_dict(self):
            return {
                'clave_docente':self.clave_docente
            }



class Inicio_Sesion(db.Model):
    __tablename__='login'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    id_docente = db.Column(db.Integer, db.ForeignKey('docente.clave_docente'), nullable= False)
    usuario = db.Column(db.Integer, nullable=False)
    contrasena = db.Column(db.Text, nullable = False)
    primera_vez = db.Column(db.Boolean,nullable=False)
    
    docente = db.relationship('Docente', backref='login')

    def to_dict(self):
        return{
            'usuario':self.usuario
        }

