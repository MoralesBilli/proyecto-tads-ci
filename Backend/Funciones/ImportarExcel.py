import pandas as pd
from Extensiones import db
from Modelos.Modelos import Alumnos, Carreras, Calificaciones, Inscripciones, Grupos,Materias
import re

#Lectura del archivo excel
def importar_calificaciones(archivo,grupos,materias):
    
    contenido = {}
    columnas_numerica = ["Unidad", "No_Faltas","Calificacion"]
    patron_no_control = r'^(?:\d{8}|[CMD]\d{8})$'
    lista_informacion = {"Grupo": grupos, "Materia":materias}


    try:
        with pd.ExcelFile(archivo) as ArchivoEx:
            hojas = ArchivoEx.sheet_names

            for hoja in hojas:
                df =archivo.parse(hoja)
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
                    
                        if df['No_Control'].duplicated().any():
                            return "No se pudo importar: hay números de control repetidos"
                        
                contenido[hoja] = df
                print(df)
                
    except Exception as e:
        return f'Error al importar el archivo: {str(e)}'
    print('guardar calificacion')
    resultado = guardar_calificaciones(contenido)
    return resultado


def importar_grupos(archivo,carreras,grupos):
    
    contenido = {}
    lista_informacion = {"Carrera":carreras, "Grupo": grupos}
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
                
                    if df['No_Control'].duplicated().any():
                        return "No se pudo importar: hay números de control repetidos"


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
    
    resultado = Guardar_Datos_grupos(contenido)
    
    return resultado
    
def guardar_calificaciones(datos):
    try:
        if isinstance(datos,dict):
            grupos = {grupo.grupo: grupo.id for grupo in Grupos.query.all()}
            materias = {materia.nombre: materia.id for materia in Materias.query.all()}

            for hoja, df in datos.items():
                nombre_grupo = df["Grupo"].iloc[0]
                id_grupo = grupos.get(nombre_grupo)
                nombre_materia = df["Materia"].iloc[0]
                id_materia=materias.get(nombre_materia)

                if id_grupo is None:
                    return f"Grupo '{nombre_grupo}' no encontrado en la base de datos"
                
                if id_materia is None:
                    return f"Grupo '{nombre_materia}' no encontrado en la base de datos"
            
            inscripciones = Inscripciones.query.filter_by(id_grupo=id_grupo).all()
            inscripciones_dict = {inc.no_control_alumno: inc.id for inc in inscripciones}

            for _, fila in df.iterrows():
                no_control = fila["No_Control"]
                unidad = int(fila["Unidad"])
                materia = fila["Materia"]
                id_inscripcion = inscripciones_dict.get(no_control)

                if id_inscripcion is None:
                    continue 
                
                calificacion_existente = Calificaciones.query.filter_by(
                    id_inscripcion=id_inscripcion,
                    unidad=unidad,
                    materia = materia
                ).first()

                if calificacion_existente:
                    # Actualizar campos
                    calificacion_existente.calificacion = fila["Calificacion"]
                    calificacion_existente.no_faltas = fila["No_Faltas"]
                    
                else:
                    # Crear nueva calificación
                    nueva_calificacion = Calificaciones(
                        id_inscripcion=id_inscripcion,
                        unidad=unidad,
                        calificacion=fila["Calificacion"],
                        no_faltas=fila["No_Faltas"],
                        materia = materia
                        
                    )
                    db.session.add(nueva_calificacion)


            db.session.commit()
            print('guardadas')
            return "Calificaciones guardadas correctamente"

        else:
            return datos
    except Exception as e:
        db.session.rollback()
        return f'No se pudo importar, error al guardar las calificaciones {str(e)}'
    

def Guardar_Datos_grupos(datos):
    try:
        if isinstance(datos,dict):
            
            carreras = {carrera.nombre: carrera.id for carrera in Carreras.query.all()}
            grupos = {grupo.grupo: grupo.id for grupo in Grupos.query.all()}
            cambios = False
            
            for hoja, df in  datos.items():
               
                for _,fila in df.iterrows():
                    

                    nombre_carrera = fila["Carrera"]
                    id_carrera = carreras.get(nombre_carrera)
                    nombre_grupo = fila["Grupo"]
                    id_grupo = grupos.get(nombre_grupo)
               
                    #guardado enla base de datos faltan los modelos
                    no_control = str(fila["No_Control"]).strip()
                    semestre_valido = str(int(fila["Semestre"]))

                    if not Alumnos.query.get(no_control):

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
                       
                   

                    inscripcion_existente = Inscripciones.query.filter_by(
                        id_grupo=id_grupo,
                        no_control_alumno=no_control
                    ).first()

                   
                    if not inscripcion_existente:
                            nueva_inscripcion = Inscripciones(
                                id_grupo = id_grupo,
                                no_control_alumno = no_control
                            )
                            db.session.add(nueva_inscripcion)
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