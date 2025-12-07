import pandas as pd
from Backend.Extensiones import db
from Modelos.Modelos import Alumnos, Carreras, Calificaciones, Inscripciones, Grupos,Materias,Docente,grupos_materias
import re
from Funciones.Agregar_docente import crear_docente
#Lectura del archivo excel

def importar_calificaciones(archivo,grupos,materias):
    
    contenido = {}
    columnas_numerica = ["Unidad", "No_Faltas","Calificación"]
    patron_no_control = r'^(?:\d{8}|[CMD]\d{8})$'
    lista_informacion = {"Grupo": grupos, "Materia":materias}
    

    try:
        with pd.ExcelFile(archivo) as ArchivoEx:
            hojas = ArchivoEx.sheet_names

            for hoja in hojas:
                df =ArchivoEx.parse(hoja)
                df.columns = df.columns.str.strip() #quita los espacios de las celdas
                
                #Revisa que existan columnas 
                faltantes = [c for c in ["Grupo"] + columnas_numerica if c not in df.columns]
                if faltantes:
                    return f"No se pudo importar, columnas faltantes, o error de escritura: {', '.join(faltantes)}"
                
                #Detecta valores nulos
                if df.isnull().values.any():
                    return "No se pudo importar, datos nulos"
                
                #Detecta valores vacios
                if (df.astype(str).apply(lambda x: x.str.strip() == "")).values.any():
                    return "No se pudo importar, datos vacíos "
                
            
                #Revisa la existencia de grupos validos
                for coex in lista_informacion:
                    if coex in df.columns:
                        df[coex] = df[coex].astype(str).str.strip()
                       
                        invalidas = ~df[coex].isin(lista_informacion[coex])
                        if invalidas.any():
                            return "No se pudo importar, grupo o materia no encontrada"
                    
                    
                #Validar que el campo unidad, calificacion y No.Faltas sea solamente numeros
                for columna in columnas_numerica:
                    if columna in df.columns:
                        no_numericos = df[~df[columna].astype(str).str.isnumeric()]
                        if not no_numericos.empty:
                            return f"No se pudo importar, datos no numéricos en {columna}"

                if 'No_Control' in df.columns:
                    
                        if not df['No_Control'].astype(str).str.match(patron_no_control).all():
                            return "No se pudo importar: hay números de control con formato inválido"
                    
                        
                        
                contenido[hoja] = df
             
                
    except Exception as e:
        return f'Error al importar el archivo: {str(e)}'
    print('guardar calificacion')
    resultado = guardar_calificaciones(contenido)
    return resultado

def importar_docentes(archivo):
    contenido = {}
    patron_nombre = r'^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s]+$'
    columnas_numerica = ['Telefono', 'Clave_Docente']
    patron_correo = r'^[a-zA-Z0-9._%+-]+@tectijuana\.edu\.mx$'
    try:
        with pd.ExcelFile(archivo) as ArchivoEx:
            hojas = ArchivoEx.sheet_names

            for hoja in hojas:
                df =ArchivoEx.parse(hoja)
                df.columns = df.columns.str.strip()
                
                #Detecta valores nulos
                if df.isnull().values.any():
                    return "No se pudo importar, datos nulos"
                
                #Detecta valores vacios
                if (df.astype(str).apply(lambda x: x.str.strip() == "")).values.any():
                    return "No se pudo importar, datos vacíos "
               
                if "Clave_Docente" in df.columns:
                    if (df['Clave_Docente'].astype(str).str.len() > 10).any():
                        return "No se pudo importar, clave docente inválida"
                    
                if 'Correo' in df.columns:
                    if ~df['Correo'].astype(str).str.match(patron_correo).all():
                        return "No se pudo importar, correo con formato incorrecto"
                    
                    if df.duplicated(subset=['Correo']).any():
                         return "No se pudo importar, datos duplicados"   

                for columna in columnas_numerica:
                    if columna in df.columns:
                        no_numericos = df[~df[columna].astype(str).str.isnumeric()]
                        if not no_numericos.empty:
                            return f"No se pudo importar, datos no numéricos en {columna}"
                
                for col in ["Nombre", "Apellido_Paterno", "Apellido_Materno"]:
                        if col in df.columns:
                            if ~df[col].astype(str).str.match(patron_nombre).all():
                                return f"No se pudo importar: hay valores inválidos en '{col}'"
                            
                limites = {
                        'Nombre': 40,
                        'Apellido_Paterno': 40,
                        'Apellido_Materno': 40
                    }
                
                for campo, max_len in limites.items():
                        if campo in df.columns:
                            if df[campo].astype(str).apply(len).gt(max_len).any():
                                return f"No se pudo importar: hay valores demasiado largos en '{campo}' (máx. {max_len} caracteres)"
                
                contenido[hoja] = df

    except Exception as e:
         return f'Error al importar el archivo: {str(e)}'
    
    resultado = guardad_docentes(contenido)
    return resultado

def importar_grupos(archivo,carreras,grupos,materias,clave_docente):
    
    contenido = {}
    lista_informacion = {"Carrera":carreras, "Grupo": grupos, "Materia":materias}
    columnas_existentes = ["Carrera","Grupo"]
    Genero = ['HOMBRE','MUJER']
    Estado_valido = ['VIGENTE', 'EGRESADO', 'BAJA_TEMPORAL', 'BAJA_DEFINITIVA']
    patron_no_control = r'^(?:\d{8}|[CMD]\d{8})$'
    patron_nombre = r'^[A-Za-zÁÉÍÓÚÜÑáéíóúüñ\s]+$'

    try:
        with pd.ExcelFile(archivo) as ArchivoEx:
            hojas = ArchivoEx.sheet_names

            for hoja in hojas:
                df =ArchivoEx.parse(hoja)
                
                

                #Detecta valores nulos
                if df.isnull().values.any():
                    return "No se pudo importar, datos nulos"
                
                #Detecta valores vacios
                if (df.astype(str).apply(lambda x: x.str.strip() == "")).values.any():
                    return "No se pudo importar, datos vacíos "
                
                #Revisa que las materias y el grupo sea valido
                for coex in columnas_existentes:
                    if coex in df.columns:
                        invalidas = ~df[coex].isin(lista_informacion[coex])
                        if coex == "Carrera" and invalidas.any():
                            return "No se pudo importar: carrera no encontrada"
                        elif coex == "Grupo" and invalidas.any():
                            return "No se pudo importar: grupo no encontrado"
                        elif coex == "Materia" and invalidas.any():
                            return "No se pudo importar: materia no encontrada"

                        
                #Revisa que el semestre sea numero
                if "Semestre" in df.columns:
                    no_numericos = df[~df["Semestre"].astype(str).str.isnumeric()]
                    if not no_numericos.empty:
                            return "No se pudo importar, datos no numéricos en 'Semestre'"
                    
                    if (df["Semestre"].astype(int) > 17).any() or (df["Semestre"].astype(int) < 1).any():
                                return "No se pudo importar: hay semestres inválidos"
                    
                #Revisa si existe un genero valido
                if 'Genero' in df.columns:
                    if not df["Genero"].isin(Genero).all():
                        return "No se pudo importar: hay un género no válido"
                    
                #Revisa que los estados sean validos
                if 'Estado' in df.columns:
                    
                    if not df['Estado'].isin(Estado_valido).all():
                        return "No se pudo importar: hay un estado invalido"

                if 'No_Control' in df.columns:
                
                    if not df['No_Control'].astype(str).str.match(patron_no_control).all():
                        return "No se pudo importar: hay números de control con formato inválido"
                   
                    
                for col in ["Nombre", "Apellido_Paterno", "Apellido_Materno"]:
                        if col in df.columns:
                            if ~df[col].astype(str).str.match(patron_nombre).all():
                                return f"No se pudo importar: hay valores inválidos en '{col}'"
                            
                limites = {
                        'Nombre': 40,
                        'Apellido_Paterno': 40,
                        'Apellido_Materno': 40
                    }
                
                for campo, max_len in limites.items():
                        if campo in df.columns:
                            if df[campo].astype(str).apply(len).gt(max_len).any():
                                return f"No se pudo importar: hay valores demasiado largos en '{campo}' (máx. {max_len} caracteres)"

                contenido[hoja] = df

    except Exception as e:
        return f'Error al importar el archivo: {str(e)}'
    
    resultado = Guardar_Datos_grupos(contenido,clave_docente)
    
    return resultado
    
def guardar_calificaciones(datos):
    try:
        cambios = False
        if not isinstance(datos, dict):
            return datos

       
        grupos = {g.grupo: g.id for g in Grupos.query.all()}
        materias = {m.nombre: m.id for m in Materias.query.all()}

        total_registros = 0

        for hoja, df in datos.items():
            nombre_grupo = df["Grupo"].iloc[0]
            nombre_materia = df["Materia"].iloc[0]
            
            id_grupo = grupos.get(nombre_grupo)
            id_materia = materias.get(nombre_materia)
           
            if id_grupo is None:
                return f"Grupo '{nombre_grupo}' no encontrado en la base de datos"
            if id_materia is None:
                return f"Materia '{nombre_materia}' no encontrada en la base de datos"

            # Obtener inscripciones del grupo
            inscripciones = Inscripciones.query.filter_by(id_grupo=id_grupo).all()
            inscripciones_dict = {str(i.no_control_alumno): i.id for i in inscripciones}

            
         
            # Obtener calificaciones existentes del grupo/materia
            calificaciones_existentes = Calificaciones.query.filter(
                Calificaciones.id_inscripcion.in_(inscripciones_dict.values()),
                Calificaciones.id_materia == id_materia
            ).all()
            
      

            calificaciones_dict = {
                (c.id_inscripcion, c.unidad): c for c in calificaciones_existentes
            }

            # Procesar cada fila del DataFrame
            for _, fila in df.iterrows():
                no_control = str(fila["No_Control"]).strip()

               

                id_inscripcion = inscripciones_dict.get(no_control)

               
                if id_inscripcion is None:
                    continue  # alumno no inscrito en este grupo

                
                unidad = int(fila["Unidad"])
                key = (id_inscripcion, unidad)
                calificacion = calificaciones_dict.get(key)

                

                if calificacion:
                    calificacion.calificacion = fila["Calificación"]
                    calificacion.faltas = fila["No_Faltas"]
                    cambios = True

                else:
                    nueva_calificacion = Calificaciones(
                        id_inscripcion=id_inscripcion,
                        unidad=unidad,
                        calificacion=fila["Calificación"],
                        faltas=fila["No_Faltas"],
                        id_materia=id_materia  
                    )
                    db.session.add(nueva_calificacion)
                    total_registros += 1
                    cambios=True
        if cambios:
            db.session.commit()
        else: 
            return f"No se pudo importar, Ninguna calificacion agregada"
        return f"Calificaciones guardadas correctamente ({total_registros} nuevas)"

    except Exception as e:
        db.session.rollback()
        return f"No se pudo importar, error al guardar las calificaciones: {str(e)}"

    

def Guardar_Datos_grupos(datos,clave_docente):

    try:
        if not isinstance(datos, dict):
            return datos
            
        carreras = {carrera.nombre: carrera.id for carrera in Carreras.query.all()}
        grupos = {grupo.grupo: grupo.id for grupo in Grupos.query.all()}
        materias = {materia.nombre: materia.id for materia in Materias.query.all()}
            

        cambios = False
        alumnos = {a.no_control: a for a in Alumnos.query.all()}
        grupo_materia = {
            (gm.id_grupo, gm.id_materia): gm
            for gm in grupos_materias.query.all()
        }
        inscripciones = {
            (i.id_grupo, i.no_control_alumno): i
            for i in Inscripciones.query.all()
        }
            
        for hoja, df in  datos.items():
               
            for _,fila in df.iterrows():
                    

                    id_carrera = carreras.get(fila["Carrera"])
                    id_grupo = grupos.get(fila["Grupo"])
                    id_materia = materias.get(fila["Materia"])
               
                   
                    no_control = str(fila["No_Control"]).strip()
                    semestre_valido = str(int(fila["Semestre"]))

                    

                    if no_control not in alumnos:

                        nuevo_alumno = Alumnos(
                            no_control=no_control,
                            nombre=fila["Nombre"],
                            apellido_paterno=fila["Apellido_Paterno"],
                            apellido_materno=fila["Apellido_Materno"],
                            genero = fila['Genero'],
                            estado=fila['Estado'],
                            semestre = semestre_valido,
                            id_carrera=id_carrera
                        )
                        db.session.add(nuevo_alumno)
                        cambios = True
                       
                   
                    key_gm = (id_grupo, id_materia)

                    

                    if key_gm not in grupo_materia:
                        nuevo_gm = grupos_materias(
                            id_grupo=id_grupo,
                            id_materia=id_materia,
                            id_docente=clave_docente
                        )
                        db.session.add(nuevo_gm)
                        grupo_materia[key_gm] = nuevo_gm
                        cambios = True

                    else:
                        gm = grupo_materia[key_gm]
                        if gm.id_docente != clave_docente:
                            gm.id_docente = clave_docente
                            cambios = True
                        
                    key_ins = (id_grupo, no_control)

                    if key_ins not in inscripciones:
                        nueva = Inscripciones(
                            id_grupo=id_grupo,
                            no_control_alumno=no_control
                        )
                        db.session.add(nueva)
                        inscripciones[key_ins] = nueva
                        cambios = True
                    

            if cambios:     
                db.session.commit()
                return "Guardado correctamente"
            else:
                return "Datos previamente guardados"

            
        else:
            return datos
    except Exception as e:
        db.session.rollback()
        return f'No se pudo importar, error al guardar los datos {str(e)}'
    
def guardad_docentes(datos):
    try:
        if isinstance(datos,dict):
            claves_existentes = {docente.clave_docente for docente in Docente.query.all()}
            for hoja, df in  datos.items():
               
                for _, fila in df.iterrows():
                    clave = fila["Clave_Docente"]
                    nombre = fila["Nombre"]
                    apellidopa = fila["Apellido_Paterno"]
                    apellidoma = fila["Apellido_Materno"]
                    telefono = fila["Telefono"]
                    correo = fila["Correo"]

                    if clave in claves_existentes:
                        continue
                    exito, mensaje = crear_docente(clave, nombre, apellidopa, apellidoma, telefono, correo)
                    if not exito:
                        return f'Error al crar los docentes {str(mensaje)}' 
                

            return "Docentes registrados"


                    
    except Exception as e:
        db.session.rollback()
        return f'No se pudo importar, error al guardar los datos {str(e)}'