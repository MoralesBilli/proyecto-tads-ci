from Backend.Extensiones import db
from flask import Blueprint, jsonify,request,send_file
from Funciones.ImportarExcel import importar_grupos,importar_calificaciones, importar_docentes
from Modelos.Modelos import Grupos, Carreras,Materias, Inicio_Sesion
import os
from Funciones.Registrar_moviminto import registrar_audi
from Funciones.Decodificar import token_required
from Funciones.Exportar_contancia import generar_reporte_tutoria
from io import BytesIO

Import_export_bp = Blueprint('Import_export',__name__)

#folder para guardar el archivo de manera temporal


@Import_export_bp.route('/api/importar/grupos',methods=['POST'])
@token_required
def importar_Excel_grupos(id_login):
    try:
        UPLOAD_FOLDER = 'grupos'
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        carreras =  Carreras.query.all()
        grupos = Grupos.query.all()
        materias = Materias.query.all()
        carreras_nombres = [carrera.nombre for carrera in carreras]
        grupos_nombres = [grupo.grupo for grupo in grupos]
        materias_nomres = [materia.nombre for materia in materias]

        docente = Inicio_Sesion.query.filter_by(id=id_login).first()
        if not docente:
            raise ValueError("No se encontró el docente con ese ID de sesión.")
        clave_docente = docente.docente.clave_docente
        
        #validaciones 
        if 'archivo' not in request.files:
            return jsonify({'error': 'No fue enviaddo un archivo'}),400
        
        archivo = request.files['archivo']

        if archivo.filename == '':
            return jsonify({'error': 'El nombre del archivo está vacío'}),400
        
        if not archivo.filename.endswith(('.xls','.xlsx')):
            return jsonify({'error':'Formato de archivo no válido'}),400
        

        ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
        archivo.save(ruta)

        procesamiento = importar_grupos(ruta,carreras_nombres,grupos_nombres,materias_nomres,clave_docente)
       
        print(procesamiento)
        os.remove(ruta)

        if procesamiento.startswith("No se pudo importar") or "Error" in procesamiento:
            return jsonify({'error': procesamiento}), 400
        
        

        id_docente=docente.id_docente

        registrar_audi('Alumnos','Importar grupo',id_docente)

        return jsonify({'message': 'Archivo procesado correctamente', 'resultado': procesamiento}),200
    except Exception  as e:
        return jsonify({'error': f'Error al importar el archivo {str(e)}'}),400


@Import_export_bp.route('/api/importar/calificaciones',methods=['POST'])
@token_required
def importar_Excel_Calificaciones(id_login):
    try:
        UPLOAD_FOLDER = 'calificacion'
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        grupos = Grupos.query.all()
        materias = Materias.query.all()
        materias_nombres = [materia.nombre for materia in materias]
        grupos_nombres = [grupo.grupo for grupo in grupos]
        #validaciones 
        if 'archivo' not in request.files:
            return jsonify({'error': 'No fue enviaddo un archivo'}),400
        
        archivo = request.files['archivo']

        if archivo.filename == '':
            return jsonify({'error': 'El nombre del archivo está vacío'}),400
        
        if not archivo.filename.endswith(('.xls','.xlsx')):
            return jsonify({'error':'Formato de archivo no válido'}),400
        

        ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
        archivo.save(ruta)

        procesamiento =  importar_calificaciones(ruta,grupos_nombres,materias_nombres)
       

        os.remove(ruta)

        if procesamiento.startswith("No se pudo importar") or "Error" in procesamiento:
            return jsonify({'error': procesamiento}), 400
        
        docente = Inicio_Sesion.query.filter_by(id=id_login).first()
        
        if not docente:
            raise ValueError("No se encontró el docente con ese ID de sesión.")
        id_docente=docente.id_docente
        registrar_audi('Alumnos','Importar calificaciones',id_docente)

        return jsonify({'mensaje':'Archivo subido', 'resultado' : procesamiento})
    except Exception  as e:
        print(str(e))
        return jsonify({'error': f'Error al importar el archivo {str(e)}'}),400


@Import_export_bp.route('/api/importar/docentes',methods=['POST'])
@token_required
def importar_Excel_Docentes(id_login):
    try:
        UPLOAD_FOLDER = 'docentes'
        os.makedirs(UPLOAD_FOLDER, exist_ok=True)
        
        #validaciones 
        if 'archivo' not in request.files:
            return jsonify({'error': 'No fue enviaddo un archivo'}),400
        
        archivo = request.files['archivo']

        if archivo.filename == '':
            return jsonify({'error': 'El nombre del archivo está vacío'}),400
        
        if not archivo.filename.endswith(('.xls','.xlsx')):
            return jsonify({'error':'Formato de archivo no válido'}),400
        

        ruta = os.path.join(UPLOAD_FOLDER, archivo.filename)
        archivo.save(ruta)

        procesamiento =  importar_docentes(ruta)
       

        os.remove(ruta)

        if procesamiento.startswith("No se pudo importar") or "Error" in procesamiento:
            return jsonify({'error': procesamiento}), 400
        
        docente = Inicio_Sesion.query.filter_by(id=id_login).first()
        if not docente:
            raise ValueError("No se encontró el docente con ese ID de sesión.")
        id_docente=docente.id_docente
        registrar_audi('Alumnos','Importar docente',id_docente)

        return jsonify({'mensaje':'Archivo subido', 'resultado' : procesamiento})
    except Exception  as e:
        return jsonify({'error': f'Error al importar el archivo {str(e)}'}),400




@Import_export_bp.route('/api/exportar/reporte_tutoria/<no_control>', methods=['GET'])
@token_required
def exportar_reporte_alumno(no_control, id_login):
    try:
        pdf_buffer = generar_reporte_tutoria(no_control)

        docente = Inicio_Sesion.query.filter_by(id=id_login).first()
        if not docente:
            raise ValueError("No se encontró el docente con ese ID de sesión.")

        registrar_audi('Alumnos', 'exportar constancia', docente.id_docente)

        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"Reporte_{no_control}.pdf"
        )

    except ValueError as e:
        return jsonify({'error': str(e)}), 404
    except Exception as e:
        return jsonify({'error': f'Ocurrió un error inesperado: {str(e)}'}), 500